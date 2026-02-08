from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from retriever.models import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_documents(self, domain: str) -> List[Document]:
        stmt = select(Document).where(Document.domain == domain)
        return list(self.db.execute(stmt).scalars().all())