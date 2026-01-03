from fastapi import APIRouter, HTTPException
from models import QueryRequest
from categorize import find_domain
import requests

from config import get_generator_url, get_retriever_urls

router = APIRouter()

@router.post("/query")
async def handle_query(req: QueryRequest):
    """
    Handle a query request by:
    1. Categorizing the query into a domain
    2. Retrieving relevant documents from the domain-specific retriever
    3. Generating an answer using the generator service
    """
    retriever_payload = {"query_text": req.query_text, "top_k": req.top_k}
    
    try:
        query_domain = find_domain(retriever_payload["query_text"])
        print(f"Query categorized as domain: {query_domain}")
        
        retriever_urls = get_retriever_urls()
        
        if query_domain not in retriever_urls:
            print(f"Unknown domain: {query_domain}. Available domains: {list(retriever_urls.keys())}")
            raise HTTPException(
                status_code=400,
                detail=f"Unknown domain: {query_domain}. Supported domains: {list(retriever_urls.keys())}"
            )
        
        retriever_url = retriever_urls[query_domain]
        print(f"Using retriever URL: {retriever_url}")

        try:
            retriever_response = requests.post(
                retriever_url,
                json=retriever_payload,
            )
            retriever_response.raise_for_status()
            retriever_res = retriever_response.json()
        except Exception as e:
            print(f"Retriever request failed: {e}")
            raise Exception(f"Retriever request failed: {e}")
        
        if "results" not in retriever_res:
            print(f"Invalid retriever response structure: {retriever_res}")
            raise Exception(f"Invalid retriever response structure: {retriever_res}")
        
        contexts = [
            {
                "id": str(doc["rank"]),
                "content": doc["document"],
                "score": doc.get("score")
            }
            for doc in retriever_res["results"]
        ]
        
        query_text = retriever_res.get("query", req.query_text)
        
        generator_payload = {
            "prompt": query_text,
            "contexts": contexts
        }

        generator_url = get_generator_url()
        try:
            generator_response = requests.post(
                generator_url,
                json=generator_payload,
            )
            generator_response.raise_for_status()
            generator_res = generator_response.json()
            return generator_res
        except Exception as e:
            print(f"Generator request failed: {e}")
            raise Exception(f"Generator request failed: {e}")

    except Exception as e:
        print(f"Unexpected error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")