# ruff: noqa: E402
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

from app.routers import generation, listings, retrieval

app = FastAPI(title="Provenance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://watch-value.vercel.app",
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