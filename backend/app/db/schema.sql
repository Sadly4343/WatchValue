CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    grade TEXT,
    size TEXT,
    jewels INTEGER,
    case_material TEXT,
    case_maker TEXT,
    running_condition TEXT,
    original_dial BOOLEAN,
    original_hands BOOLEAN,
    case_condition_notes TEXT,
    sold_price NUMERIC NOT NULL,
    sold_date DATE NOT NULL,
    source TEXT DEFAULT 'personal_observation',
    listing_url TEXT,
    description TEXT
);

CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    source_type TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB
);

CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);