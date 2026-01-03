import os
from dotenv import load_dotenv

# Only load .env file if not running in Kubernetes (where Secret provides env vars)
if not os.getenv("KUBERNETES_SERVICE_HOST"):
    print("Load .env file for local development")
    load_dotenv()  # Load .env for local development

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "google/gemma-2b")