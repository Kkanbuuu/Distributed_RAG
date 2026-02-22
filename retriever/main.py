from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine

from retriever import SimpleRetriever
from config import get_database_url, get_domain
from repository.document_repository import DocumentRepository


class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 5

class AddDocumentRequest(BaseModel):
    title: str
    content: str
    domain: str
    source_url: str | None = None

app = FastAPI()

engine = create_engine(get_database_url())
repository = DocumentRepository(engine)
retriever = SimpleRetriever(
    document_repository=repository,
    domain=get_domain(),
)


@app.get("/")
def root():
    return {"message": "Simple Retriever is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/add-document")
def add_document(req: AddDocumentRequest):
    """Add a document to the repository."""
    doc = retriever.add_document(
        title=req.title,
        content=req.content,
        domain=req.domain,
        source_url=req.source_url,
    )
    return {"message": "ok", "id": doc.id, "title": doc.title}

@app.post("/query")
def query(req: QueryRequest):
    results = retriever.query(req.query_text, top_k=req.top_k)
    return {"query": req.query_text, "results": results}