from difflib import SequenceMatcher


def token_similarity(tokens1, tokens2):
    return SequenceMatcher(None, tokens1, tokens2).ratio()


def detect_type2_clones(files, threshold=0.8):
    clones = []

    n = len(files)

    for i in range(n):
        for j in range(i + 1, n):

            sim = token_similarity(files[i]["tokens"], files[j]["tokens"])

            if sim >= threshold:
                clones.append({
                    "file1": files[i]["file_path"],
                    "file2": files[j]["file_path"],
                    "similarity": round(sim, 2),
                    "type": "Type 2 (Token Similarity)"
                })

    return clones