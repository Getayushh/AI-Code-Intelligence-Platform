import os
import google.generativeai as genai

# ✅ Reads API key from environment variable
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


# # 1. Initialize the client
# client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# # 2. Use the EXACT name from your list
# result = client.models.embed_content(
#     model="models/gemini-embedding-001", 
#     contents="test"
# )
def get_embeddings_batch(texts: list) -> list:
    """
    Get embeddings for a list of code strings using Gemini API.
    Returns a list of embedding vectors (each is a list of floats).
    """
    embeddings = []
    for text in texts:
        try:
            # Truncate very long files to avoid token limit errors
            truncated = text[:8000] if len(text) > 8000 else text

            result = genai.embed_content(
                model="models/text-embedding-001",
                content=truncated,
                task_type="SEMANTIC_SIMILARITY"
            )
            embeddings.append(result["embedding"])
        except Exception as e:
            print(f"[Warning] Embedding failed for a file: {e}")
            # Return zero vector as fallback (768 dims for text-embedding-004)
            embeddings.append([0.0] * 768)

    return embeddings
