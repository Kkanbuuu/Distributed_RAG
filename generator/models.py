from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    id: str
    content: str
    score: Optional[float] = None
    source: Optional[str] = None


class GenerateRequest(BaseModel):
    prompt: str
    contexts: List[Document]

class GenerateResponse(BaseModel):
    answer: str
    model: str
    latency_ms: Optional[float] = None