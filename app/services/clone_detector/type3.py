"""
Type 3 Clone Detection — AST-Based (Structural Similarity)
Compares the sequence of AST node types between two files.
"""
import ast


def extract_ast_sequence(code: str) -> list:
    """Return a flat list of AST node type names from the code."""
    try:
        tree = ast.parse(code)
        return [type(node).__name__ for node in ast.walk(tree)]
    except SyntaxError:
        return []


def ast_similarity(seq_a: list, seq_b: list) -> float:
    """Jaccard similarity on AST node-type sets."""
    if not seq_a or not seq_b:
        return 0.0

    set_a = set(seq_a)
    set_b = set(seq_b)

    intersection = set_a & set_b
    union = set_a | set_b

    return len(intersection) / len(union) if union else 0.0


def detect_type3_clones(files: list, threshold: float = 0.80) -> list:
    clones = []
    n = len(files)

    ast_seqs = [extract_ast_sequence(f["clean_code"]) for f in files]

    for i in range(n):
        for j in range(i + 1, n):
            sim = ast_similarity(ast_seqs[i], ast_seqs[j])
            if sim >= threshold:
                clones.append([
                    files[i]["file_path"],
                    files[j]["file_path"]
                ])

    return clones
