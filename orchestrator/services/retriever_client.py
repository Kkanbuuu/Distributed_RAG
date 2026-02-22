import asyncio
import httpx
import requests
from config import get_retriever_urls

class RetrieverClient:
    def __init__(self):
        self.retriever_urls = get_retriever_urls()

    def retrieve(self, query_domain: str, query_text: str, top_k: int):
        retriever_url = self.retriever_urls[query_domain]
        retriever_payload = {
            "query_text": query_text,
            "top_k": top_k
        }
        try :
            retriever_response = requests.post(retriever_url, json=retriever_payload)
            retriever_response.raise_for_status()
            return retriever_response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Retriever request failed: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Retriever request failed: {e}") from e
        except Exception as e:
            raise Exception(f"Retriever request failed: {e}")
    
    async def retrieve_single_domain_async(self, query_domain: str, client: httpx.AsyncClient, query_text: str, top_k: int):
        retriever_url = self.retriever_urls[query_domain]
        retriever_payload = {
            "query_text": query_text,
            "top_k": top_k
        }
        try: 
            response = await client.post(retriever_url, json=retriever_payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Retriever request failed: {e.response.status_code}")
        except httpx.RequestError as e:
            raise Exception(f"Retriever request failed: {e}")
        except Exception as e:
            raise Exception(f"Retriever request failed: {e}")

    async def retrieve_multiple_domains(self, query_text: str, top_k: int) -> list[dict]:
        contexts = []
        domains = self.get_retriever_urls().keys()    
        async with httpx.AsyncClient() as client:
            tasks = [
                self.retrieve_single_domain(domain, client, query_text, top_k) for domain in domains
            ]  

            results = await asyncio.gather(*tasks)
            return results