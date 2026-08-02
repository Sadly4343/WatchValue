from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.routers import listings, retrieval, generation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Provenance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://watch-value-34xed54d5-logan-hartshorns-projects.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(listings.router)
app.include_router(retrieval.router)
app.include_router(generation.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}