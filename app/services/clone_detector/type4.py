import numpy as np
from app.services.model_singleton import get_embeddings_batch


def cosine_similarity(vec_a, vec_b) -> float:
    a = np.array(vec_a)
    b = np.array(vec_b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def detect_type4_clones(files: list, threshold: float = 0.90) -> list:
    if len(files) < 2:
        return []

    codes = [f["clean_code"] for f in files]

    # ✅ Single batch API call instead of loading a local model
    embeddings = get_embeddings_batch(codes)

    clones = []
    n = len(files)

    for i in range(n):
        for j in range(i + 1, n):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            if sim >= threshold:
                clones.append([
                    files[i]["file_path"],
                    files[j]["file_path"]
                ])

    return clones
