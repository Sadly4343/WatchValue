from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.services.embeddings import embed_text
from app.services.generation import (
    build_prompt,
    extract_entities,
    generate_answer,
    get_price_stats,
    vector_search,
)

router = APIRouter(prefix="/generation", tags=["generation"])

@router.get("/")
def generate_valuation(question: str, db: Session = Depends(get_db)):
    query_vector = embed_text(question)
    entities = extract_entities(question, db)
    matches = vector_search(query_vector, db)

    if not entities["manufacturer"] or not entities["model"]:
        return {
            "question": question,
            "answer": (
                "I couldn't identify a specific manufacturer and model in your question. "
                "Try including both, like 'Waltham Vanguard'."
            ),
            "matches": matches,
        }
    price_stats = get_price_stats(entities["manufacturer"], entities["model"], db)
    prompt = build_prompt(question, price_stats, matches)
    answer = generate_answer(prompt)

    return {
        "question": question,
        "answer": answer,
        "price_stats": price_stats,
        "matches": matches,
    }
    
