from pydantic import BaseModel, Field
from typing import Optional, Any

class ChatResponse(BaseModel):
    response: str = Field(..., description="The AI's response")
    source_documents: Optional[list[Any]] = Field(None, description="Source documents used for RAG")
