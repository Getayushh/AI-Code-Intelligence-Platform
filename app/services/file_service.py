import os
import zipfile
import shutil
from fastapi import UploadFile
from app.services.preprocess import preprocess_code

UPLOAD_DIR = "temp_uploads"

from app.services.clone_detector.type1 import detect_type1_clones
from app.services.clone_detector.type2 import detect_type2_clones
from app.services.clone_detector.type3 import detect_type3_clones
from app.services.clone_detector.type4 import detect_type4_clones

from app.services.clustering_service import cluster_files
from app.services.insights_service import generate_insights

async def process_uploaded_zip(file: UploadFile):
    
    # Step 1: Create temp directory
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)

    # Step 2: Save uploaded ZIP
    zip_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(zip_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Step 3: Extract ZIP
    extract_path = os.path.join(UPLOAD_DIR, "extracted")
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Step 4: Collect Python files
    python_files = []

    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                  code = f.read()
                  processed = preprocess_code(code)

                python_files.append({
                  "file_path": full_path,
                  "clean_code": processed["clean_code"],
                  "tokens": processed["tokens"]
                })

    

    type1_clones = detect_type1_clones(python_files)
    type2_clones = detect_type2_clones(python_files)
    type3_clones = detect_type3_clones(python_files)
    type4_clones = detect_type4_clones(python_files)
    clusters = cluster_files(python_files)

    return {
        "total_files": len(python_files),
        "type1_clones": type1_clones,
        "type2_clones": type2_clones,
        "type3_clones": type3_clones,
        "type4_clones": type4_clones,
        "clusters": clusters

    }
    insights = generate_insights(result)

    result["insights"] = insights

    return result