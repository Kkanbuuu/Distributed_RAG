from typing import List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from models import Document
from repository import DocumentRepository


class SimpleRetriever:
    def __init__(
        self,
        document_repository: DocumentRepository,
        domain: str,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.repository = document_repository
        self.domain = domain
        self.model = SentenceTransformer(model_name)
        self.documents: List[Document] = []
        self.embeddings = None
        self.index = None
        self._load_data()
        self._embed_documents()

    def _load_data(self) -> None:
        # Load documents from PostgreSQL based on the domain (for now)
        # TODO: Load documents based on the domain received from orchestrator
        self.documents = self.repository.get_documents(self.domain)
        print(f"Loaded {len(self.documents)} documents from PostgreSQL (domain={self.domain}).")

    def _embed_documents(self) -> None:
        if not self.documents:
            print("No documents to embed.")
            self.embeddings = None
            self.index = None
            return
        contents = [doc.content for doc in self.documents]
        self.embeddings = self.model.encode(
            contents,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True,
        )
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.embeddings.astype("float32"))
        print(f"Indexed {len(self.documents)} documents.")

    def query(self, query_text: str, top_k: int = 5) -> List[dict]:
        if self.index is None or len(self.documents) == 0:
            return []
        query_embedding = self.model.encode(
            [query_text], convert_to_numpy=True, normalize_embeddings=True
        ).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for i, idx in enumerate(indices[0]):
            doc = self.documents[idx]
            print(f"Document: {doc.id} (Score: {float(distances[0][i])})")
            results.append({
                "rank": i + 1,
                "document": doc.content,
                "document_id": doc.id,
                "title": doc.title,
                "domain": doc.domain,
                "score": float(distances[0][i]),
            })
        return results
