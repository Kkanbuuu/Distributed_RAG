CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    domain TEXT NOT NULL,
    version INT NOT NULL DEFAULT 1,
    source_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- 384 dims for all-MiniLM-L6-v2; nullable until backfilled
    embedding vector(384) 
);

CREATE INDEX idx_documents_domain ON documents (domain);
CREATE INDEX idx_documents_title ON documents (title);

-- HNSW index for cosine similarity search (<=> operator)
CREATE INDEX idx_documents_embedding ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);