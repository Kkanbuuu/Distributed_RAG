from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine

from retriever import SimpleRetriever
from config import get_database_url, get_domain
from repository.document_repository import DocumentRepository


class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 5


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

@app.get("/load_data")
def load_data():
    retriever._load_data()
    retriever._embed_documents()
    return {"message": "Data loaded successfully.", "num_documents": len(retriever.documents)}

@app.post("/query")
def query(req: QueryRequest):
    results = retriever.query(req.query_text, top_k=req.top_k)
    return {"query": req.query_text, "results": results}