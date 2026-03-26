import re
import tokenize
import io


def remove_comments(code: str) -> str:
    """
    Removes comments from Python code
    """
    # Remove single-line comments
    code = re.sub(r"#.*", "", code)

    # Remove multi-line comments (docstrings)
    code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", "", code, flags=re.DOTALL)

    return code


def normalize_whitespace(code: str) -> str:
    """
    Normalize spaces and newlines
    """
    code = re.sub(r"\s+", " ", code)
    return code.strip()


def tokenize_code(code: str):
    """
    Convert code into tokens
    """
    tokens = []
    try:
        token_generator = tokenize.generate_tokens(io.StringIO(code).readline)
        for tok in token_generator:
            tokens.append(tok.string)
    except Exception:
        pass

    return tokens


def preprocess_code(code: str):
    """
    Full preprocessing pipeline
    """
    code = remove_comments(code)
    code = normalize_whitespace(code)
    tokens = tokenize_code(code)

    return {
        "clean_code": code,
        "tokens": tokens
    }