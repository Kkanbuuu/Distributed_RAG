from sqlalchemy import literal_column, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from typing import List

from models import Document


class DocumentRepository:
    def __init__(self, engine: Engine):
        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_documents(self, domain: str) -> List[Document]:
        with self._session_factory() as session:
            stmt = select(Document).where(Document.domain == domain)
            return list(session.execute(stmt).scalars().all())

    def get_all_documents(self) -> List[Document]:
        with self._session_factory() as session:
            stmt = select(Document)
            return list(session.execute(stmt).scalars().all())

    def add_document(
        self,
        title: str,
        content: str,
        domain: str,
        embedding: List[float],
        source_url: str | None = None,
    ) -> Document:
        """Insert a document with precomputed embedding."""
        doc = Document(
            title=title,
            content=content,
            domain=domain,
            source_url=source_url,
            embedding=embedding,
        )
        with self._session_factory() as session:
            session.add(doc)
            session.commit()
            session.refresh(doc) # To ensure the document is committed and has an ID
        return doc

    def search_by_vector(
        self,
        query_embedding: List[float],
        domain: str,
        top_k: int = 5,
    ) -> List[dict]:
        """
        pgvector ORM: cosine_distance(<=>) 계산 후 상위 top_k 반환.
        Returns [{rank, document, document_id, title, domain, score}, ...]
        """
        distance = Document.embedding.cosine_distance(query_embedding)
        score_expr = (literal_column("1") - distance).label("score")
        with self._session_factory() as session:
            stmt = (
                select(Document, score_expr)
                .where(Document.domain == domain)
                .where(Document.embedding.isnot(None))
                .order_by(distance)
                .limit(top_k)
            )
            rows = session.execute(stmt).all()
        return [
            {
                "rank": i + 1,
                "document": doc.content,
                "document_id": str(doc.id),
                "title": doc.title,
                "domain": doc.domain,
                "score": float(score),
            }
            for i, (doc, score) in enumerate(rows)
        ]