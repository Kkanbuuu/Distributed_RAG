CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    domain TEXT NOT NULL,
    version INT NOT NULL DEFAULT 1,
    source_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_domain ON documents (domain);
CREATE INDEX idx_documents_created_at ON documents (created_at);
CREATE INDEX idx_documents_updated_at ON documents (updated_at);
CREATE INDEX idx_documents_title ON documents (title);
CREATE INDEX idx_documents_content ON documents (content);
CREATE INDEX idx_documents_source_url ON documents (source_url);