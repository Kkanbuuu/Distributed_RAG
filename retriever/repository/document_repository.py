from sqlalchemy import select
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

            