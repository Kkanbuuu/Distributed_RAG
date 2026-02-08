from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from typing import List

from retriever.models import Document


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