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

    def add_document(
        self,
        title: str,
        content: str,
        domain: str,
        source_url: str | None = None,
    ) -> Document:
        """1) content를 model로 임베딩, 2) repository.add_document로 저장."""
        embedding = self.model.encode(
            [content], convert_to_numpy=True, normalize_embeddings=True
        ).tolist()[0] 
        return self.repository.add_document(
            title=title,
            content=content,
            domain=domain,
            embedding=embedding,
            source_url=source_url,
        )

    def query(self, query_text: str, top_k: int = 5) -> List[dict]:
        """" Encode the query text and search the repository."""
        query_embedding = self.model.encode(
            [query_text], convert_to_numpy=True, normalize_embeddings=True
        ).tolist()[0]
        results = self.repository.search_by_vector(query_embedding, self.domain, top_k)
        print(f"Retrieved {len(results)} documents.")
        for result in results:
            print(f"Document: {result['title']} (Score: {result['score']})")
        return results
