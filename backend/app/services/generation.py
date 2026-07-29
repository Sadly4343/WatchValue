import os
from anthropic import Anthropic
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import text

from app.models.listing import Listing

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_entities(question: str, db: Session) -> dict:
    question_lower = question.lower()

    manufacturers = [row[0] for row in db.query(Listing.manufacturer).distinct().all()]
    models = [row[0] for row in db.query(Listing.model).distinct().all()]

    matched_manufacturer = next((m for m in manufacturers if m.lower() in question_lower), None)
    matched_model = next((mo for mo in models if mo.lower() in question_lower), None)

    return {"manufacturer": matched_manufacturer, "model": matched_model}

def get_price_stats(manufacturer: str, model: str, db: Session) -> dict:
    result = db.query(
        func.avg(Listing.sold_price),
        func.min(Listing.sold_price),
        func.max(Listing.sold_price),
        func.count(Listing.id),
    ).filter(
        Listing.manufacturer == manufacturer,
        Listing.model == model,
    ).first()

    avg_price, min_price, max_price, count = result
    return {"avg": avg_price, "min": min_price, "max": max_price, "count": count}



def vector_search(query_vector: list[float], db: Session, limit: int = 5) -> list[dict]:
    result = db.execute(
        text("""
            SELECT chunk_text, source_id, embedding <=> :query_vector AS distance
            FROM document_chunks
            ORDER BY distance
            LIMIT :limit
        """),
        {"query_vector": str(query_vector), "limit": limit}
    )
    return [{"chunk_text": row.chunk_text, "source_id": row.source_id, "distance": row.distance} for row in result]

def build_prompt(question: str, price_stats: dict, matches: list[dict]) -> str:
    context_lines = "\n".join(f"- {m['chunk_text']}" for m in matches)

    prompt = f"""A user is asking about vintage watch valuation.

Question: {question}

Price statistics from comparable sales:
- Average price: ${price_stats['avg']}
- Price range: ${price_stats['min']} - ${price_stats['max']}
- Number of comparable sales: {price_stats['count']}

Relevant listing descriptions:
{context_lines}

Instructions:
- Only use the price statistics and listing descriptions provided above. Do not add outside information about the brand, model, or market beyond what's given here.
- If the number of comparable sales is low, say so explicitly rather than presenting the price as a confident market average.
- Be concise and cite specific details from the listings where relevant.

Answer:"""

    return prompt

def generate_answer(prompt: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text