from config import get_generator_url
import requests

class GeneratorClient:
    def __init__(self):
        self.url = get_generator_url()

    def generate(self, contexts: list[dict], query_text: str):
        print(f"[generator_client] Generating answer for query: {query_text}")
        print(f"[generator_client] Contexts: {contexts}")
        generator_payload = {
            "prompt": query_text,
            "contexts": contexts
        }
        try:
            generator_response = requests.post(
                self.url, 
                json=generator_payload
            )
            generator_response.raise_for_status()
            return generator_response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Generator request failed: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Generator request failed: {e}")