import json
import numpy as np
from sentence_transformers import SentenceTransformer


with open("domain_samples.json", "r", encoding="utf-8") as f:
    domain_samples = json.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

domain_embeddings = {}

for domain, queries in domain_samples.items():
    embeddings = model.encode(queries)
    domain_embeddings[domain] = np.mean(embeddings, axis=0)
    print(f"{domain} embeddings done")
print("All embeddings done")
