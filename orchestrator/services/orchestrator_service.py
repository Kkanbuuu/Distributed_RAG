from .retriever_client import RetrieverClient
from .generator_client import GeneratorClient


class OrchestratorService:
    """
    Service layer for orchestrating RAG queries.
    Fan-out: retrieves from all domain retrievers in parallel, then generates answer.
    """
    
    def __init__(self):
        self.retriever_client = RetrieverClient()
        self.generator_client = GeneratorClient()

    async def process_query(self, query_text: str, top_k: int):
        """
        Process a query through the RAG pipeline:
        1. Fan-out: retrieve from all retrievers in parallel (retrieve_multiple_domains)
        2. Merge results and build contexts
        3. Generate answer
        
        Args:
            query_text: The user's query
            top_k: Number of top results per retriever
            
        Returns:
            Generator response with answer
        """
        results = await self.retriever_client.retrieve_multiple_domains(query_text, top_k)
        print(f"[orchestrator] Retrieved {len(results)} docs, building contexts")
        contexts = [
            {
                "id": f"{doc.get('domain', '')}_{doc.get('rank', i)}",
                "content": doc["document"],
                "score": doc.get("score"),
            }
            for i, doc in enumerate(results)
        ]
        print(f"[orchestrator] Sending {len(contexts)} contexts to generator")
        return self.generator_client.generate(contexts, query_text)