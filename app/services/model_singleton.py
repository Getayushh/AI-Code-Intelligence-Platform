import os
from google import genai



def get_embeddings_batch(texts: list) -> list:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("[Warning] GEMINI_API_KEY not set")
        return None

    client = genai.Client(api_key=api_key)
    print(f"[DEBUG Embeddings] Processing {len(texts)} texts")  # ← add this

    embeddings = []
    for text in texts:
        try:
            truncated = text[:8000] if len(text) > 8000 else text
            result = client.models.embed_content(
                model="models/gemini-embedding-2-preview",
                contents=truncated
            )
            embeddings.append(result.embeddings[0].values)
            print(f"[DEBUG Embeddings] Success, size: {len(result.embeddings[0].values)}")  # ← add this
        except Exception as e:
            print(f"[Warning] Embedding failed: {e}")
            embeddings.append([0.0] * 3072)

    return embeddings