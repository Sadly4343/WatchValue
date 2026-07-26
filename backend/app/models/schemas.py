from datetime import date
from pydantic import BaseModel


class ListingCreate(BaseModel):
    manufacturer: str
    model: str
    grade: str | None = None
    size: str | None = None
    jewels: int | None = None

    case_material: str | None = None
    case_maker: str | None = None

    running_condition: str | None = None
    original_dial: bool | None = None
    original_hands: bool | None = None
    case_condition_notes: str | None = None

    sold_price: float
    sold_date: date
    source: str = "personal_observation"
    listing_url: str | None = None

    description: str | None = None


class ListingResponse(ListingCreate):
    id: int

    class Config:
        from_attributes = True