"""
Type 3 Clone Detection — AST-Based (Structural Similarity)
Compares the sequence of AST node types between two files.
"""
import ast
from collections import Counter


def extract_ast_sequence(code: str) -> list:
    try:
        tree = ast.parse(code)
        return [type(node).__name__ for node in ast.walk(tree)]
    except SyntaxError:
        return []


def ast_similarity(seq_a: list, seq_b: list) -> float:
    if not seq_a or not seq_b:
        return 0.0
    
    # ✅ Use Counter-based similarity instead of set — preserves frequency
    counter_a = Counter(seq_a)
    counter_b = Counter(seq_b)
    
    intersection = sum((counter_a & counter_b).values())
    total = sum(counter_a.values()) + sum(counter_b.values())
    
    return (2 * intersection) / total if total > 0 else 0.0


def detect_type3_clones(files: list, threshold: float = 0.95) -> list:
    clones = []
    n = len(files)
    ast_seqs = [extract_ast_sequence(f.get("raw_code", f["clean_code"])) for f in files]

    for i in range(n):
        for j in range(i + 1, n):
            sim = ast_similarity(ast_seqs[i], ast_seqs[j])
            if sim >= threshold:
                clones.append({
                    "file1": files[i]["file_path"],
                    "file2": files[j]["file_path"],
                    "similarity": round(sim * 100, 1)
                })

    return clones