# orchestrator.py
from fastapi import FastAPI
from models import QueryRequest
from categorize import find_domain
import requests
import os

from dotenv import load_dotenv
load_dotenv()

GENERATOR_URL = os.getenv("GENERATOR_URL")

RETRIEVER_URLS = {
    "news": os.getenv("RETRIEVER_NEWS_URL"),
    "finance": os.getenv("RETRIEVER_FINANCE_URL"),
    "law": os.getenv("RETRIEVER_LAW_URL"),
}

app = FastAPI(title="RAG Orchestrator")

@app.get("/health")
async def health():
    return {"message": "Orchestrator is running"}

@app.post("/query")
async def handle_query(req: QueryRequest):
    retriever_payload = {"query_text": req.query_text, "top_k": req.top_k}
    
    # 1. Categorizes query into domain
    query_domain = find_domain(retriever_payload["query_text"])
    print(f'domain: {query_domain}')
    retriever_url = RETRIEVER_URLS[query_domain]
    print(f'retriever url: {retriever_url}')

    # 2. Calls Retriever
    # retriever_res = requests.post(RETRIEVER_URL, json=retriever_payload).json()
    retriever_res = requests.post(retriever_url, json=retriever_payload).json()
    print(retriever_res)
    contexts = [
        {"id": str(doc["rank"]), "content": doc["document"], "score": doc.get("score")}
        for doc in retriever_res["results"]
        ]
    generator_payload = {
            "prompt": retriever_res["query"],
            "contexts": contexts
        }

    # 3. Pass to Generator
    generator_res = requests.post(GENERATOR_URL, json=generator_payload).json()
    return generator_res