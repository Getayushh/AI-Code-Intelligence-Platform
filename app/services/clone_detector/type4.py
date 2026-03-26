from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once (IMPORTANT)
model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(code):
    return model.encode(code)


def detect_type4_clones(files, threshold=0.85):
    clones = []

    n = len(files)

    embeddings = []

    # Step 1: Generate embeddings
    for file in files:
        emb = get_embedding(file["clean_code"])
        embeddings.append(emb)

    # Step 2: Compare embeddings
    for i in range(n):
        for j in range(i + 1, n):

            sim = cosine_similarity(
                [embeddings[i]],
                [embeddings[j]]
            )[0][0]

            if sim >= threshold:
                clones.append({
                    "file1": files[i]["file_path"],
                    "file2": files[j]["file_path"],
                    "similarity": round(float(sim), 2),
                    "type": "Type 4 (Semantic Similarity)"
                })

    return clones