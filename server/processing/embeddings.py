from typing import List

from config import openai_client


def embed_text(text: str) -> List[float]:
    if len(text) > 3000:
        text = text[:3000]
    resp = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return resp.data[0].embedding
