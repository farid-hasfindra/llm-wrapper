from fastapi import APIRouter, Depends, HTTPException, Header
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from app.llm.groq_client import groq_client
from app.rag.pipeline import generate_rag_response
from app.core.security import get_api_key
from app.core.logging import logger

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, 
    api_key: str = Depends(get_api_key),
    x_user_id: str = Header("guest")
):
    """
    Chat with the LLM via the Orchestrator.
    """
    try:
        from app.orchestration.orchestrator import orchestrator
        return await orchestrator.handle_request(request, user_id=x_user_id)
            
    except Exception as e:
        logger.error("chat_endpoint_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
