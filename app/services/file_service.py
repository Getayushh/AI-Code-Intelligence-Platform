import os
import zipfile
import shutil
import tempfile
import pathlib
from fastapi import UploadFile, HTTPException

# Import services
from app.services.preprocess import preprocess_code
from app.services.clone_detector.type1 import detect_type1_clones
from app.services.clone_detector.type2 import detect_type2_clones
from app.services.clone_detector.type3 import detect_type3_clones
from app.services.clone_detector.type4 import detect_type4_clones
from app.services.clustering_service import cluster_files
from app.services.insights_service import generate_insights


# Before — inside project dir, always watched:
UPLOAD_DIR = "temp_uploads"

# After — in /tmp, completely outside uvicorn's watch scope:
UPLOAD_DIR = str(pathlib.Path(tempfile.gettempdir()) / "ai_code_intel_uploads")


# 🔧 Convert numpy types → Python native types
def convert_numpy(obj):
    import numpy as np

    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    else:
        return obj


async def process_uploaded_zip(file: UploadFile):
    """
    Full pipeline with error handling
    """

    # 🔹 Step 1: Validate input
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed")

    # 🔹 Step 2: Clean temp directory
    try:
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)
        os.makedirs(UPLOAD_DIR)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to prepare upload directory: {str(e)}")

    # 🔹 Step 3: Save uploaded file
    try:
        zip_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(zip_path, "wb") as f:
            content = await file.read()
            f.write(content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {str(e)}")

    # 🔹 Step 4: Extract ZIP
    extract_path = os.path.join(UPLOAD_DIR, "extracted")

    try:
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ZIP extraction failed: {str(e)}")

    # 🔹 Step 5: Read & preprocess Python files
    python_files = []

    try:
        for root, dirs, files in os.walk(extract_path):
            for filename in files:
                if filename.endswith(".py"):
                    full_path = os.path.join(root, filename)

                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            code = f.read()
                            processed = preprocess_code(code)

                        python_files.append({
                            "file_path": full_path,
                            "clean_code": processed["clean_code"],
                            "tokens": processed["tokens"]
                        })

                    except Exception as e:
                        print(f"[Warning] Skipping file {full_path}: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    # 🔹 Edge Case: No Python files
    if len(python_files) == 0:
        raise HTTPException(status_code=400, detail="No Python files found in ZIP")

    # 🔹 Step 6: Clone Detection
    try:
        type1_clones = detect_type1_clones(python_files)
        type2_clones = detect_type2_clones(python_files)
        type3_clones = detect_type3_clones(python_files)
        type4_clones = detect_type4_clones(python_files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clone detection failed: {str(e)}")

    # 🔹 Step 7: Clustering
    try:
        clusters = cluster_files(python_files)
    except Exception as e:
        print(f"[Warning] Clustering failed: {e}")
        clusters = []

    # 🔹 Step 8: Combine Results
    result = {
        "total_files": len(python_files),
        "type1_clones": type1_clones,
        "type2_clones": type2_clones,
        "type3_clones": type3_clones,
        "type4_clones": type4_clones,
        "clusters": clusters
    }

    # 🔹 Step 9: Insights
    try:
        insights = generate_insights(result)
        result["insights"] = insights
    except Exception as e:
        print(f"[Warning] Insights generation failed: {e}")
        result["insights"] = {
            "summary": "Insights generation failed",
            "risk_level": "Unknown",
            "insights": [],
            "suggestions": []
        }

    # 🔹 Step 10: Fix numpy serialization
    try:
        result = convert_numpy(result)
    except Exception as e:
        print(f"[Warning] Numpy conversion failed: {e}")

    return result