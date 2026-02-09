from app.schemas.request import ChatRequest

class Router:
    """
    Decides the best path for a request.
    Example paths:
    - Direct LLM (General chitchat)
    - RAG (Knowledge base queries)
    - Tool (Calculator, Search, etc.)
    """
    
    async def route_request(self, request: ChatRequest) -> str:
        # Simple Logic for now
        if request.use_rag:
            return "rag"
        
        # Future: Use LLM classifier
        # prompt = f"Classify this query: {request.message}"
        # ...
        
        return "direct_llm"
