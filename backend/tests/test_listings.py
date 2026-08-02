from datetime import date

from app.db.base import SessionLocal
from app.models.listing import Listing


def test_create_and_read_listing():
    db = SessionLocal()
    try:
        listing = Listing(
            manufacturer="Waltham",
            model="1883",
            sold_price=250.00,
            sold_date=date(2026, 1, 1),
            source="personal_observation",
        )
        db.add(listing)
        db.commit()
        db.refresh(listing)

        assert listing.id is not None

        fetched = db.query(Listing).filter(Listing.id == listing.id).first()
        assert fetched is not None
        assert fetched.manufacturer == "Waltham"
        assert fetched.sold_price == 250.00

    finally:
        if listing.id is not None:
            db.query(Listing).filter(Listing.id == listing.id).delete()
            db.commit()
        db.close()