# orchestrator.py
from fastapi import FastAPI
from models import QueryRequest
from categorize import find_domain
import requests
import os

from dotenv import load_dotenv

if not os.getenv("KUBERNETES_SERVICE_HOST"):
    load_dotenv()  

def get_generator_url():
    return os.getenv("GENERATOR_URL")

def get_retriever_urls():
    return {
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
    
    # Get retriever URLs dynamically (always reads current env vars)
    retriever_urls = get_retriever_urls()
    retriever_url = retriever_urls[query_domain]
    print(f'retriever url: {retriever_url}')

    # 2. Calls Retriever
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
    generator_url = get_generator_url()
    try:
        response = requests.post(generator_url, json=generator_payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        generator_res = response.json()
        return generator_res
        
    except Exception as e:
        print(f"Generator error: {e}")
        raise