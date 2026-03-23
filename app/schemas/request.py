from pydantic import BaseModel, Field
from typing import Optional, List

class MessageSchema(BaseModel):
    role: str = Field(..., description="Role of the message sender (user or ai)")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message")
    use_rag: bool = Field(False, description="Whether to use RAG for this request")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for memory (not yet implemented)")
    model: Optional[str] = Field(None, description="The specific LLM mode to use")
    chat_history: Optional[List[MessageSchema]] = Field(default_factory=list, description="Previous messages in the conversation")
    system_prompt: Optional[str] = Field(None, description="Optional custom system prompt to override default persona")
