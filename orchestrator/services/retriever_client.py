import asyncio
from typing import List

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
            print(f"[retriever_client] Requesting domain: {query_domain}")
            response = await client.post(retriever_url, json=retriever_payload)
            response.raise_for_status()
            data = response.json()
            n = len(data.get("results") or [])
            print(f"[retriever_client] Domain {query_domain}: got {n} results")
            return data
        except httpx.HTTPStatusError as e:
            print(f"[retriever_client] Domain {query_domain} failed: HTTP {e.response.status_code}")
            raise Exception(f"Retriever request failed: {e.response.status_code}")
        except httpx.RequestError as e:
            print(f"[retriever_client] Domain {query_domain} failed: {e}")
            raise Exception(f"Retriever request failed: {e}")
        except Exception as e:
            print(f"[retriever_client] Domain {query_domain} failed: {e}")
            raise Exception(f"Retriever request failed: {e}")

    async def retrieve_multiple_domains(self, query_text: str, top_k: int) -> List[dict]:
        """
        Fan-out: call all retrievers in parallel, merge results.
        Returns list of result dicts (each includes "domain"). Failed domains are skipped.
        """
        domains = list(self.retriever_urls.keys())
        print(f"[retriever_client] Fan-out: query to {len(domains)} domains (top_k={top_k}): {domains}")
        async with httpx.AsyncClient() as client:
            tasks = [
                self.retrieve_single_domain_async(domain, client, query_text, top_k)
                for domain in domains
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        merged: List[dict] = []
        for domain, r in zip(domains, results):
            if isinstance(r, Exception):
                print(f"[retriever_client] Skipping domain {domain} (exception)")
                continue
            if r and "results" in r:
                for doc in r["results"]:
                    merged.append({**doc, "domain": domain})
        print(f"[retriever_client] Fan-out done: {len(merged)} total results from {len(domains)} domains")
        return merged