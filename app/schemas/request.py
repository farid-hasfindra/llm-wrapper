from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message")
    use_rag: bool = Field(False, description="Whether to use RAG for this request")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for memory (not yet implemented)")
