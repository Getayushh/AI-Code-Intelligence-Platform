import ast


def get_ast_representation(code):
    try:
        tree = ast.parse(code)
        return ast.dump(tree)
    except Exception:
        return ""


def detect_type3_clones(files, threshold=0.85):
    clones = []

    n = len(files)

    ast_representations = []

    # Step 1: Convert all files to AST
    for file in files:
        ast_repr = get_ast_representation(file["clean_code"])
        ast_representations.append(ast_repr)

    # Step 2: Compare ASTs
    for i in range(n):
        for j in range(i + 1, n):

            if not ast_representations[i] or not ast_representations[j]:
                continue

            similarity = (
                len(set(ast_representations[i]) & set(ast_representations[j]))
                / len(set(ast_representations[i]) | set(ast_representations[j]))
            )

            if similarity >= threshold:
                clones.append({
                    "file1": files[i]["file_path"],
                    "file2": files[j]["file_path"],
                    "similarity": round(similarity, 2),
                    "type": "Type 3 (AST Similarity)"
                })

    return clones