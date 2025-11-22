# orchestrator.py
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="RAG Orchestrator")

# Retriever / Generator URL (Kubernetes Service 이름 기준)
RETRIEVER_URL = "http://retriever-service:8000/query"
# GENERATOR_URL = "http://generator-service:8000/generate"

class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 5

class GeneratorResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {"message": "Orchestrator is running"}

@app.post("/query")
def handle_query(req: QueryRequest):
    # 1. Calls Retriever
    retriever_payload = {"query_text": req.query_text, "top_k": req.top_k}
    retriever_res = requests.post(RETRIEVER_URL, json=retriever_payload).json()
    context_chunks = [r["document"] for r in retriever_res.get("results", [])]

    return {"query": req.query_text, "results": retriever_res, "context_chunks": context_chunks}