from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.listing import Listing, DocumentChunk
from app.models.schemas import ListingCreate, ListingResponse
from app.services.embeddings import text_builder, embed_text

router = APIRouter(prefix="/listings", tags=["listings"])


@router.post("/", response_model=ListingResponse)
def create_listing(payload: ListingCreate, db: Session = Depends(get_db)):
    listing = Listing(**payload.model_dump())
    db.add(listing)
    db.commit()
    db.refresh(listing)

    text = text_builder(payload)
    embedding = embed_text(text)

    chunk = DocumentChunk(
        source_type="listing_description",
        source_id=listing.id,
        chunk_text=text,
        embedding=embedding,
    )
    db.add(chunk)
    db.commit()

    return listing

@router.post("/bulk", response_model=list[ListingResponse])
def create_listings_bulk(payload: list[ListingCreate], db: Session = Depends(get_db)):
    created_listings = []

    for item in payload:
        listing = Listing(**item.model_dump())
        db.add(listing)
        db.flush()

        text = text_builder(item)
        embedding = embed_text(text)

        chunk = DocumentChunk(
            source_type="listing_description",
            source_id=listing.id,
            chunk_text=text,
            embedding=embedding
        )
        db.add(chunk)

        created_listings.append(listing)
        
    db.commit()

    for listing in created_listings:
        db.refresh(listing)
    
    return created_listings




@router.get("/", response_model=list[ListingResponse])
def get_listings(
    manufacturer: str | None = None,
    model: str | None = None,
    jewels: int | None = None,
    size: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Listing)
    if manufacturer:
        query = query.filter(Listing.manufacturer == manufacturer)
    if model:
        query = query.filter(Listing.model == model)
    if jewels:
        query = query.filter(Listing.jewels == jewels)
    if size:
        query = query.filter(Listing.size == size)
    return query.all()