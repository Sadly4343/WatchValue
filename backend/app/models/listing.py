from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, Text, JSON
from pgvector.sqlalchemy import Vector

from app.db.base import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)
    grade = Column(String, nullable=True)
    size = Column(String, nullable=True)
    jewels = Column(Integer, nullable=True)

    case_material = Column(String, nullable=True)
    case_maker = Column(String, nullable=True)

    running_condition = Column(String, nullable=True)
    original_dial = Column(Boolean, nullable=True)
    original_hands = Column(Boolean, nullable=True)
    case_condition_notes = Column(Text, nullable=True)

    sold_price = Column(Numeric, nullable=False)
    sold_date = Column(Date, nullable=False)
    source = Column(String, default="personal_observation")
    listing_url = Column(String, nullable=True)

    description = Column(Text, nullable=True)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String, nullable=False)
    source_id = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(Vector(1536))
    metadata_ = Column("metadata", JSON, nullable=True)