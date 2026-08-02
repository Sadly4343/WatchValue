# Provenance

[![CI](https://github.com/Sadly4343/WatchValue/actions/workflows/ci.yml/badge.svg)](https://github.com/Sadly4343/WatchValue/actions/workflows/ci.yml)

A RAG (Retrieval-Augmented Generation) app for vintage watch valuation. Ask a question like *"what's a fair price for a Waltham Vanguard 16 size in good condition?"* and get an answer grounded in real comparable sale data — not model guesswork.

**Live app:** [watch-value.vercel.app](https://watch-value.vercel.app)
**API docs:** [watchvalue-production.up.railway.app/docs](https://watchvalue-production.up.railway.app/docs)

## How it works

1. Your question is embedded and matched against stored listing descriptions (vector search)
2. The manufacturer/model is identified and real price stats (avg/min/max/count) are pulled from SQL
3. Claude combines both to write a grounded answer — it's instructed to use only the retrieved data, never outside knowledge

```
Question ──► embedding ──► vector search ──► matching listings
    │                                              │
    └──► SQL lookup ──► price stats ───────────────┴──► Claude ──► answer
```

**Why hybrid retrieval?** Prices come from real SQL math, not LLM guessing — this removes hallucination risk on the numbers that matter. Descriptive context comes from semantic search over free-text listings. If sample size is low, the prompt tells Claude to say so rather than presenting one data point as a market average.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | FastAPI (Python), deployed on Railway |
| Frontend | React + Vite, deployed on Vercel |
| Database | PostgreSQL + pgvector |
| ORM / Migrations | SQLAlchemy + Alembic |
| Embeddings | OpenAI `text-embedding-3-small` |
| Generation | Anthropic Claude API |
| CI/CD | GitHub Actions (lint, type-check, tests, migrations) + Docker Compose for local dev |

## Project structure

```
backend/
├── app/
│   ├── main.py            # FastAPI entrypoint
│   ├── db/base.py         # SQLAlchemy engine/session
│   ├── models/             # SQLAlchemy models + Pydantic schemas
│   ├── routers/             # listings, retrieval, generation endpoints
│   └── services/             # embeddings + RAG pipeline logic
├── alembic/                 # DB migrations
├── tests/                   # pytest suite
├── Dockerfile
└── requirements.txt

frontend/
├── src/                     # React app (search UI + bulk listing form)
└── Dockerfile

.github/workflows/ci.yml     # CI: lint, type-check, migrations, tests, build
docker-compose.yml           # local dev: backend + frontend + db
```

## API endpoints

| Endpoint | What it does |
|---|---|
| `POST /listings/` | Create a listing (auto-generates its embedding) |
| `GET /listings/` | Filter listings by manufacturer, model, jewels, size |
| `GET /retrieval/?question=...` | Vector search only, no LLM call |
| `GET /generation/?question=...` | Full RAG pipeline → grounded answer |

Example response from `/generation/`:
```json
{
  "question": "what is a fair price for a Waltham Vanguard 16 size",
  "answer": "Based on the available data, a fair price appears to be around $225...",
  "price_stats": { "avg": 225, "min": 225, "max": 225, "count": 1 },
  "matches": [{ "chunk_text": "...", "source_id": 1, "distance": 0.29 }]
}
```

## Running locally

**Prerequisites:** Docker Desktop, an OpenAI API key, an Anthropic API key

```bash
git clone <repo-url>
cd WatchValue
cp .env.example .env   # fill in your API keys and DB URL
docker compose up --build
```

- Backend: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

Migrations run via Alembic:
```bash
docker compose exec backend alembic upgrade head
```

Run tests / lint / type-check:
```bash
docker compose exec backend bash
pytest -v
ruff check .
mypy .
```

## CI/CD

Every push and PR to `main` runs automatically via GitHub Actions:
- `ruff` (lint) and `mypy` (type-check)
- Alembic migrations against a fresh Postgres+pgvector service container
- Full `pytest` suite
- Frontend build check

Deploys are separate: **Railway** (backend, from `backend/Dockerfile`) and **Vercel** (frontend), both connected to auto-deploy on push to `main`.

## Design decisions

- **SQL owns the numbers, vector search owns the context** — prices are never LLM-estimated
- **Grounded generation** — Claude is instructed to use only retrieved data, never outside brand/market knowledge
- **Low sample size is surfaced, not hidden** — the prompt calls it out explicitly rather than faking confidence
- **Cost-aware short-circuiting** — unrecognized manufacturer/model questions skip the Claude call entirely
- **Manual data entry over scraping** — avoids ToS/legal risk while still being genuine RAG (retrieval architecture defines RAG, not data source)

## Roadmap

- [x] Ingestion pipeline (listing creation + embedding)
- [x] Hybrid retrieval (SQL + vector search)
- [x] Grounded generation
- [x] React frontend
- [x] Deployment (Railway + Vercel)
- [x] CI/CD (GitHub Actions)
- [ ] Authentication

## License

Personal portfolio project.
