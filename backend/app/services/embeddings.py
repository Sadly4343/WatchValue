import os
from openai import OpenAI
from app.models.schemas import ListingCreate

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-small"

def text_builder(payload: ListingCreate) -> str:
    parts = [
        f"{payload.manufacturer} {payload.model}",
        f"{payload.size}" if payload.size else None,
        f"{payload.jewels}" if payload.jewels else None,
        f"{payload.case_material}" if payload.case_material else None,
        f"{payload.running_condition}" if payload.running_condition else None,
        f"{payload.description}" if payload.description else None,
        f"{payload.grade}" if payload.grade else None,
    ]
    text = " ".join(filter(None, parts))
    return text


def embed_text(text: str) -> list[float]:
  
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding