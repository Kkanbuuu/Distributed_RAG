import requests
from config import get_retriever_urls

class RetrieverClient:
    def __init__(self):
        self.url = get_retriever_urls()

    def get_retriever_url(self, domain: str):
        if domain not in self.url:
            raise ValueError(f"Unknown domain: {domain}")
        return self.url[domain]

    def retrieve(self, query_domain: str, query_text: str, top_k: int):
        retriever_url = self.get_retriever_url(query_domain)
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