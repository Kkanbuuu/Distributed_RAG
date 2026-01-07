from categorize import find_domain
from config import get_generator_url, get_retriever_urls
import requests
from .retriever_client import RetrieverClient

class OrchestratorService:
    """
    Service layer for orchestrating RAG queries.
    Handles the business logic of categorizing queries, retrieving documents,
    and generating answers.
    """
    
    def __init__(self):
        self.retriever_client = RetrieverClient()

    def process_query(self, query_text: str, top_k: int):
        """
        Process a query through the RAG pipeline:
        1. Categorize query into domain
        2. Retrieve relevant documents
        3. Generate answer
        
        Args:
            query_text: The user's query
            top_k: Number of top results to retrieve
            
        Returns:
            Generator response with answer
            
        Raises:
            ValueError: If domain is unknown or configuration is invalid
            Exception: If retriever or generator service fails
        """
        
        try:
            query_domain = find_domain(query_text)
            print(f"Query categorized as domain: {query_domain}")

            retriever_res = self.retriever_client.retrieve(query_domain, query_text, top_k)
            
            if "results" not in retriever_res:
                print(f"Invalid retriever response structure: {retriever_res}")
                raise Exception(f"Invalid retriever response structure: {retriever_res}")        
                
        except Exception as e:
            print(f"Retriever request failed: {e}")
            raise Exception(f"Retriever request failed: {e}")
        
        contexts = [
            {
                "id": str(doc["rank"]),
                "content": doc["document"],
                "score": doc.get("score")
            }
            for doc in retriever_res["results"]
        ]
        
        query_text_for_generator = retriever_res.get("query", query_text)
        
        generator_payload = {
            "prompt": query_text_for_generator,
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