import os
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
MODEL_NAME = os.getenv("MODEL_NAME", "google/gemma-2b")