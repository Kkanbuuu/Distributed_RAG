from embeddings import model, domain_embeddings
from scipy.spatial.distance import cosine

def find_domain(query_text: str) -> str:
    query_vec = model.encode([query_text])[0]

    best_domain = None
    best_score = -1
    for domain, emb in domain_embeddings.items():
        score = 1 - cosine(query_vec, emb)  # similarity
        if score > best_score:
            best_score = score
            best_domain = domain
    return best_domain          # e.g. "finance"