from pydantic import BaseModel
from typing import Optional, List, Any

class TokenUsageSchema(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float

class SourceDocument(BaseModel):
    content: str
    metadata: dict

class ChatResponse(BaseModel):
    response: str
    rag_enabled: bool = False
    sources: List[SourceDocument] = []
    usage: Optional[TokenUsageSchema] = None
