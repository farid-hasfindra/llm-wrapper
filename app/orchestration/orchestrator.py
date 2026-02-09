from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse, TokenUsageSchema
from app.llm.gemini_client import gemini_client
from app.rag.pipeline import generate_rag_response
from app.core.logging import logger
from app.llm.token_manager import token_manager

class Orchestrator:
    """
    The brain of the operation. Orchestrates the flow of data between:
    - User Request
    - Security/Policy Check (Future)
    - RAG / Vector Store
    - LLM
    - Memory (Future)
    """
    
    async def handle_request(self, request: ChatRequest, user_id: str = "anonymous") -> ChatResponse:
        logger.info("orchestrator_handling_request", user_id=user_id, task="chat")
        
        # 1. Routing Decision (Simple logic for now: User flag)
        # Future: Use an LLM or classifier to decide if RAG is needed
        use_rag = request.use_rag
        
        # 2. Execution
        if use_rag:
            # RAG Flow
            # Currently RAG pipeline returns just a string
            response_text = await generate_rag_response(request.message)
            
            # Estimate tokens for RAG (Refactor TODO: Make RAG pipeline return actual usage)
            prompt_tokens = token_manager.estimate_tokens(request.message) 
            completion_tokens = token_manager.estimate_tokens(response_text)
            usage_stats = token_manager.create_usage_report(prompt_tokens, completion_tokens)
            
            # Convert to schema
            usage_schema = TokenUsageSchema(
                prompt_tokens=usage_stats.prompt_tokens,
                completion_tokens=usage_stats.completion_tokens,
                total_tokens=usage_stats.total_tokens,
                estimated_cost=usage_stats.estimated_cost
            )
            
            return ChatResponse(
                response=response_text, 
                rag_enabled=True,
                usage=usage_schema
                # Todo: pipe sources from RAG pipeline
            )
        else:
            # Direct LLM Flow
            llm_result = await gemini_client.generate_response(request.message)

            usage_data = llm_result["usage"]
            
            usage_schema = TokenUsageSchema(
                prompt_tokens=usage_data.prompt_tokens,
                completion_tokens=usage_data.completion_tokens,
                total_tokens=usage_data.total_tokens,
                estimated_cost=usage_data.estimated_cost
            )
            
            return ChatResponse(
                response=llm_result["content"],
                rag_enabled=False,
                usage=usage_schema
            )

orchestrator = Orchestrator()
