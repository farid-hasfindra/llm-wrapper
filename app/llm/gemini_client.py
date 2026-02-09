from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.core.logging import logger

class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7):
        if not settings.GOOGLE_API_KEY:
            logger.warning("GOOGLE_API_KEY not set. Gemini features will not work.")
        
        self.model_name = model_name
        self.temperature = temperature
        self._llm = None

    @property
    def llm(self):
        if not self._llm:
            self._llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=self.temperature,
                convert_system_message_to_human=True 
            )
        return self._llm

    async def generate_response(self, prompt: str) -> dict:
        try:
            logger.info("generating_response", model=self.model_name)
            # ainvoke returns an AIMessage object which contains response_metadata
            response = await self.llm.ainvoke(prompt)
            
            content = response.content
            usage_metadata = response.response_metadata.get("usage_metadata", {})
            
            # Extract actual token counts from Gemini response if available
            prompt_tokens = usage_metadata.get("prompt_token_count", 0)
            candidates_token_count = usage_metadata.get("candidates_token_count", 0) # Output tokens
            
            # If 0 (e.g. some models don't return it), estimate it
            if prompt_tokens == 0:
                 prompt_tokens = len(prompt) // 4
            if candidates_token_count == 0:
                 candidates_token_count = len(content) // 4

            from app.llm.token_manager import token_manager
            usage_stats = token_manager.create_usage_report(prompt_tokens, candidates_token_count)
            
            return {
                "content": content,
                "usage": usage_stats
            }

        except Exception as e:
            logger.error("gemini_generation_failed", error=str(e))
            raise e

gemini_client = GeminiClient()
