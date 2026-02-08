from sentence_transformers import SentenceTransformer
import numpy as np
import os
import faiss

class SimpleRetriever:
    def __init__(self, data_dir: str, model_name: str = 'all-MiniLM-L6-v2'):
        self.data_dir = data_dir
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = None
        self._load_data()
        self._embed_documents()

    def _load_data(self):
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(self.data_dir, filename), 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            self.documents.append(line)
        print(f"Loaded {len(self.documents)} documents from {self.data_dir}.")

    def _embed_documents(self):
        self.embeddings = self.model.encode(self.documents, convert_to_numpy=True, show_progress_bar=True, normalize_embeddings=True)
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.embeddings.astype('float32'))
        print(f"Indexed {len(self.documents)} documents.")

    def query(self, query_text: str, top_k: int = 5):
        if self.embeddings is None:
            self._embed_documents()
            
        query_embedding = self.model.encode([query_text], convert_to_numpy=True, normalize_embeddings=True).astype('float32')

        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "rank": i + 1,
                "document": self.documents[idx],
                "score": float(distances[0][i])
            })
        return results
