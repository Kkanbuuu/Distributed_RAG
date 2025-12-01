from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    id: str
    content: str
    score: Optional[float] = None

class QueryRequest(BaseModel):
    query_text: str
    top_k: int = 5

class GeneratorResponse(BaseModel):
    answer: str