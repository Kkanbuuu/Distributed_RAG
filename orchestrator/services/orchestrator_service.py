from categorize import find_domain
from .retriever_client import RetrieverClient
from .generator_client import GeneratorClient

class OrchestratorService:
    """
    Service layer for orchestrating RAG queries.
    Handles the business logic of categorizing queries, retrieving documents,
    and generating answers.
    """
    
    def __init__(self):
        self.retriever_client = RetrieverClient()
        self.generator_client = GeneratorClient()

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
            ValueError: If domain is unknown, configuration invalid, or response structure invalid
            Exception: If retriever or generator service fails (propagated from clients)
        """
        query_domain = find_domain(query_text)
        print(f"Query categorized as domain: {query_domain}")

        retriever_res = self.retriever_client.retrieve(query_domain, query_text, top_k)
        
        if "results" not in retriever_res:
            raise ValueError(f"Invalid retriever response structure: missing 'results' key")
        
        contexts = [
            {
                "id": str(doc["rank"]),
                "content": doc["document"],
                "score": doc.get("score")
            }
            for doc in retriever_res["results"]
        ]

        prompt = retriever_res.get("query", query_text)
        
        generator_res = self.generator_client.generate(contexts, prompt)
        return generator_res