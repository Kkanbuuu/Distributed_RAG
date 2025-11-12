import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from retriever import SimpleRetriever

retriever = SimpleRetriever(data_dir="data")

query = "삼성전자 주가"
results = retriever.query(query, top_k=3)

print(f"\n[Query] {query}")
print("="*40)
for r in results:
    print(f"Rank {r['rank']} | Score: {r['score']:.4f}")
    print(f"→ {r['document']}\n")