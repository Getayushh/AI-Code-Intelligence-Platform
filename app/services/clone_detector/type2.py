"""
Type 2 Clone Detection — Token-Based
Normalizes identifiers/literals and compares token sequences.
"""


def normalize_tokens(tokens: list) -> list:
    """Replace variable names and string/number literals with placeholders."""
    normalized = []
    import tokenize

    NAME_PLACEHOLDER = "VAR"
    STRING_PLACEHOLDER = "STR"
    NUMBER_PLACEHOLDER = "NUM"

    # We use a simple heuristic: replace NAME tokens that look like identifiers
    # and all STRING / NUMBER tokens
    keywords = {
        "def", "class", "return", "import", "from", "if", "else", "elif",
        "for", "while", "try", "except", "finally", "with", "as", "pass",
        "break", "continue", "and", "or", "not", "in", "is", "None",
        "True", "False", "lambda", "yield", "raise", "del", "global",
        "nonlocal", "assert", "async", "await",
    }

    for tok in tokens:
        if tok in keywords or tok in "()[]{}:.,=+-*/%<>!&|^~@":
            normalized.append(tok)
        elif tok.startswith(("'", '"')):
            normalized.append(STRING_PLACEHOLDER)
        elif tok.replace(".", "").replace("_", "").isdigit():
            normalized.append(NUMBER_PLACEHOLDER)
        elif tok.isidentifier() and tok not in keywords:
            normalized.append(NAME_PLACEHOLDER)
        else:
            normalized.append(tok)

    return normalized


def token_similarity(tokens_a: list, tokens_b: list) -> float:
    """Jaccard similarity on token n-grams (bigrams)."""
    if not tokens_a or not tokens_b:
        return 0.0

    def bigrams(tokens):
        return set(zip(tokens, tokens[1:]))

    bg_a = bigrams(tokens_a)
    bg_b = bigrams(tokens_b)

    if not bg_a and not bg_b:
        return 1.0

    intersection = bg_a & bg_b
    union = bg_a | bg_b

    return len(intersection) / len(union)


def detect_type2_clones(files: list, threshold: float = 0.85) -> list:
    clones = []
    n = len(files)

    normalized = [normalize_tokens(f["tokens"]) for f in files]

    for i in range(n):
        for j in range(i + 1, n):
            sim = token_similarity(normalized[i], normalized[j])
            if sim >= threshold:
                clones.append([
                    files[i]["file_path"],
                    files[j]["file_path"]
                ])

    return clones
