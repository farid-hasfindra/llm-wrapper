from fastapi import APIRouter, Depends, HTTPException
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from app.llm.gemini_client import gemini_client
from app.rag.pipeline import generate_rag_response
from app.core.security import get_api_key
from app.core.logging import logger

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(get_api_key)):
    """
    Chat with the LLM. Optionally use RAG.
    """
    try:
        logger.info("request_received", use_rag=request.use_rag)
        
        if request.use_rag:
            response_text = await generate_rag_response(request.message)
            # Todo: Return source documents if needed.
            return ChatResponse(response=response_text)
        else:
            response_text = await gemini_client.generate_response(request.message)
            return ChatResponse(response=response_text)
            
    except Exception as e:
        logger.error("chat_endpoint_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
