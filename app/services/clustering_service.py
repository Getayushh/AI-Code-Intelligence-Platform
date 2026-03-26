from sklearn.cluster import DBSCAN
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def cluster_files(files, eps=0.3, min_samples=2):
    
    # Step 1: Generate embeddings
    embeddings = []
    file_paths = []

    for file in files:
        emb = model.encode(file["clean_code"])
        embeddings.append(emb)
        file_paths.append(file["file_path"])

    embeddings = np.array(embeddings)

    # Step 2: Apply DBSCAN
    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric='cosine'
    ).fit(embeddings)

    labels = clustering.labels_

    # Step 3: Group into clusters
    clusters = {}

    for idx, label in enumerate(labels):
        if label == -1:
            continue  # noise

        if label not in clusters:
            clusters[label] = []

        clusters[label].append(file_paths[idx])

    # Convert to list format
    result = []
    for cluster_id, files in clusters.items():
        result.append({
            "cluster_id": cluster_id,
            "files": files,
            "size": len(files)
        })

    return result