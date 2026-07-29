from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.generation import vector_search
from app.db.base import get_db

from app.services.embeddings import embed_text
from app.models.schemas import ListingResponse

router = APIRouter(prefix="/retrieval", tags=["retrieval"])

@router.get("/")
def search_listings(question: str, db: Session = Depends(get_db)):
    query_vector = embed_text(question)
    matches = vector_search(query_vector, db)

    return {"question": question, "matches": matches}

    

    
