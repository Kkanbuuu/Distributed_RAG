import os
from dotenv import load_dotenv

# Only load .env file if not running in Kubernetes (where ConfigMap provides env vars)
if not os.getenv("KUBERNETES_SERVICE_HOST"):
    load_dotenv()

def get_generator_url() -> str:
    url = os.getenv("GENERATOR_URL")
    if not url:
        raise ValueError("GENERATOR_URL environment variable is not set")
    return url

def get_retriever_urls() -> dict[str, str]:
    urls = {
        "overview": os.getenv("RETRIEVER_OVERVIEW_URL"),
        "concepts": os.getenv("RETRIEVER_CONCEPTS_URL"),
    }
    
    missing = [domain for domain, url in urls.items() if not url]
    if missing:
        raise ValueError(f"Missing retriever URLs for domains: {', '.join(missing)}")
    
    return urls
