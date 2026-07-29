from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.routers import listings, retrieval, generation

app = FastAPI(title="Provenance API")

app.include_router(listings.router)
app.include_router(retrieval.router)
app.include_router(generation.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}