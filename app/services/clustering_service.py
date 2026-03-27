import numpy as np
from sklearn.cluster import DBSCAN
from app.services.model_singleton import get_embeddings_batch


def cluster_files(files, eps=0.3, min_samples=2):

    codes = [f["clean_code"] for f in files]
    file_paths = [f["file_path"] for f in files]

    # ✅ Single batch API call instead of loading a local model
    embeddings = np.array(get_embeddings_batch(codes))

    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric='cosine'
    ).fit(embeddings)

    labels = clustering.labels_

    cluster_map = {}
    for idx, label in enumerate(labels):
        if label == -1:
            continue
        label = int(label)
        if label not in cluster_map:
            cluster_map[label] = []
        cluster_map[label].append(file_paths[idx])

    result = []
    for cluster_id, file_list in cluster_map.items():
        result.append({
            "cluster_id": cluster_id,
            "files": file_list,
            "size": int(len(file_list))
        })

    return result
