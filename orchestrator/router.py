from fastapi import APIRouter
from models import QueryRequest

from categorize import find_domain
import requests


router = APIRouter()


# Retriever / Generator URL (Kubernetes Service 이름 기준)
RETRIEVER_URL = "http://retriever-service:8000/query"
GENERATOR_URL = "http://generator-service:8800/generate"

RETRIEVER_URLS = {
    "news": "http://news-retriever-service:8000/query",
    "finance": "http://finance-retriever-service:8000/query",
    "law": "http://law-retriever-service:8000/query"
}

@router.post("/query")
async def handle_query(req: QueryRequest):
    retriever_payload = {"query_text": req.query_text, "top_k": req.top_k}
    
    # 1. Categorizes query into domain
    query_domain = find_domain(retriever_payload["query_text"])
    retriever_url = RETRIEVER_URLS[query_domain]


    # 2. Calls Retriever
    # retriever_res = requests.post(RETRIEVER_URL, json=retriever_payload).json()
    retriever_res = requests.post(retriever_url, json=retriever_payload).json()
    contexts = [
        {"id": str(doc["rank"]), "content": doc["document"], "score": doc.get("score")}
        for doc in retriever_res
        ]
    generator_payload = {
            "prompt": req.query_text,  # 사용자가 입력한 query
            "contexts": contexts
        }

    # 3. Pass to Generator
    generator_res = requests.post(GENERATOR_URL, json=generator_payload).json()
    return generator_res