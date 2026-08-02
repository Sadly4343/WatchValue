# Provenance

A hybrid RAG (Retrieval-Augmented Generation) application for vintage watch valuation and authentication. Provenance combines structured SQL price data with semantic vector search to give grounded, data-backed answers to watch valuation questions — powered by real comparable sale data, not model guesswork.

**Live app:** [watch-value.vercel.app](https://watch-value.vercel.app)
**Live API docs:** [watchvalue-production.up.railway.app/docs](https://watchvalue-production.up.railway.app/docs)

## What it does

Ask a natural-language question like *"what's a fair price for a Waltham Vanguard 16 size in good condition?"* and Provenance:

1. Embeds your question and finds the most semantically similar listing descriptions in the database (vector search)
2. Identifies the manufacturer/model mentioned in your question and pulls real price statistics (avg/min/max/count) from structured sales data (SQL)
3. Passes both — the real numbers and the relevant context — to Claude, which composes a clear, grounded answer

The price is always computed by SQL, never guessed by the LLM. Claude's job is to explain the data, not invent it.

## Architecture

**Hybrid retrieval, not pure vector search.** Watch listings are stored two ways:

- **`listings` table** — structured fields (manufacturer, model, grade, size, jewels, case material, condition, sold price, sold date, etc.) for fast, accurate SQL aggregation
- **`document_chunks` table** — free-text descriptions converted to vector embeddings (pgvector) for semantic similarity search

This split means numeric answers (price ranges, averages) come from real database math, while descriptive/qualitative context comes from semantic search over listing text. The LLM only synthesizes what's retrieved — it's explicitly instructed not to add outside knowledge about brands or markets, keeping answers grounded and traceable back to actual data.

### Pipeline

```
User question
     │
     ├──► OpenAI embedding ──► pgvector similarity search ──► relevant listing descriptions
     │
     └──► Vocabulary match (manufacturer/model) ──► SQL aggregate query ──► price stats
                                                              │
                                                              ▼
                                              Claude (grounded prompt) ──► final answer
```

## Tech stack

- **Backend:** FastAPI (Python), deployed on Railway
- **Frontend:** React (Vite), deployed on Vercel
- **Database:** PostgreSQL + pgvector extension — Docker locally, Railway Postgres in production
- **ORM:** SQLAlchemy
- **Embeddings:** OpenAI `text-embedding-3-small`
- **Generation:** Anthropic Claude API
- **Containerization:** Docker Compose (local dev)

## Project structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entrypoint, router registration
│   ├── db/
│   │   └── base.py             # SQLAlchemy engine/session setup
│   ├── models/
│   │   ├── listing.py          # SQLAlchemy models (Listing, DocumentChunk)
│   │   └── schemas.py          # Pydantic request/response schemas
│   ├── routers/
│   │   ├── listings.py         # POST/GET /listings — create & filter listings
│   │   ├── retrieval.py        # GET /retrieval — vector search only
│   │   └── generation.py       # GET /generation — full RAG pipeline
│   └── services/
│       ├── embeddings.py       # text_builder + embed_text (OpenAI)
│       └── generation.py       # entity extraction, price stats, vector search,
│                                # prompt building, Claude call
├── db/
│   └── schema.sql              # Postgres schema (listings, document_chunks, pgvector index)
├── docker-compose.yml
├── requirements.txt
└── .env                        # OPENAI_API_KEY, ANTHROPIC_API_KEY, DATABASE_URL (not committed)

frontend/
├── src/
│   ├── App.jsx                 # Bulk listing entry form + search/valuation UI
│   ├── App.css
│   └── main.jsx
├── package.json
└── .env                        # VITE_API_URL (not committed)
```

## Frontend

Two features live in one page:

- **Watch Valuation Search** — a search box that hits `GET /generation/`, rendering Claude's markdown-formatted answer, price stats, and the source listings it drew from.
- **Add Watch Listings** — a dynamic multi-row form for bulk-logging observed sales. Each row auto-collapses to a one-line summary (`Manufacturer — Model — $Price`) when a new row is added, and stays clickable to re-expand and edit. Submits the whole batch to `POST /listings/bulk` in one request, then resets to a single blank row.

## Deployment

- **Frontend** deploys to Vercel from the `frontend/` directory, with `VITE_API_URL` set to the live Railway backend URL.
- **Backend** deploys to Railway from the `backend/` directory (root directory set accordingly), with `DATABASE_URL` pointing at Railway's Postgres via `${{ Postgres.DATABASE_URL }}`, plus `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` set as environment variables. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- **Database** is Railway's managed Postgres, with the `vector` extension and schema (`listings`, `document_chunks`, HNSW index) applied manually via Railway's query interface on first setup.
- **CORS** (`app/main.py`) explicitly allowlists both the local dev origin (`http://localhost:5173`) and the deployed frontend's stable production URL — never a wildcard, and never a per-deployment preview URL (those change on every deploy).

## Setup

### Prerequisites
- Docker Desktop
- Python 3.11+
- An OpenAI API key
- An Anthropic API key

### 1. Clone and install
```bash
git clone <repo-url>
cd provenance-rag/backend
pip install -r requirements.txt
```

### 2. Environment variables
Create a `.env` file in `backend/`:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/provenance
```

### 3. Start the database
```bash
docker compose up -d
```
This spins up Postgres with pgvector and runs `db/schema.sql` on first init to create the `listings` and `document_chunks` tables.

> **Note:** the schema only runs on the *first* container start with a fresh volume. If you need to reset it (e.g., after a schema change), run `docker compose down -v` first to wipe the volume, then `docker compose up -d` again.

### 4. Run the API
```bash
uvicorn app.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`.

## API Endpoints

### `POST /listings/`
Create a new listing. Automatically generates and stores an embedding of the listing description.

```json
{
  "manufacturer": "Waltham",
  "model": "Vanguard",
  "size": "16s",
  "jewels": 21,
  "sold_price": 225,
  "sold_date": "2026-07-20",
  "description": "Vanguard 16 size, 21 jewel, gold-filled case, running well, minor case wear"
}
```

### `GET /listings/`
Filter listings by manufacturer, model, jewels, or size.

### `GET /retrieval/?question=...`
Vector similarity search only — returns the closest matching listing descriptions with cosine distance scores. No LLM call.

### `GET /generation/?question=...`
Full RAG pipeline — embeds the question, runs vector search, extracts manufacturer/model, pulls SQL price stats, and returns a Claude-generated answer grounded in that data.

```json
{
  "question": "what is a fair price for a Waltham Vanguard 16 size",
  "answer": "Based on the available data, a fair price appears to be around $225...",
  "price_stats": { "avg": 225, "min": 225, "max": 225, "count": 1 },
  "matches": [ { "chunk_text": "...", "source_id": 1, "distance": 0.29 } ]
}
```

## Design decisions worth noting

- **SQL owns the numbers, vector search owns the context.** Price statistics are never computed or estimated by the LLM — they come directly from aggregate SQL queries. This eliminates hallucination risk on the numbers that matter most.
- **Grounded generation.** The prompt explicitly instructs Claude to use only the provided data and not supplement with outside brand/market knowledge, preserving RAG's core guarantee: answers are traceable to real, stored data.
- **Low sample size is surfaced, not hidden.** If only one or two comparable sales exist, the prompt instructs Claude to say so explicitly rather than presenting a single data point as a confident market average.
- **Cost-aware short-circuiting.** If a question doesn't match a known manufacturer/model, the generation endpoint returns early without calling Claude, avoiding wasted API spend on a query that can't produce a useful answer.
- **Manual data entry over scraping.** Listing data is entered from manually observed sold listings rather than scraped from marketplaces like eBay, avoiding ToS and legal risk while still qualifying as a genuine RAG architecture — RAG is defined by retrieval architecture, not by data provenance.

## Roadmap

- [x] Ingestion pipeline (listing creation + embedding)
- [x] Hybrid retrieval (SQL + vector search)
- [x] Grounded generation (Claude-composed answers)
- [x] React frontend (bulk listing form + search/valuation UI)
- [x] Deployment (Railway + Vercel)
- [ ] Authentication

## License

Personal portfolio project.
