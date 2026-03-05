from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.logging import logger

class GroqClient:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.7):
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set. Chat generation will fail.")
        
        self.model_name = model_name
        self.temperature = temperature
        self._llm = None

    @property
    def llm(self):
        if not self._llm:
            self._llm = ChatOpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=settings.GROQ_API_KEY,
                model_name=self.model_name,
                temperature=self.temperature,
            )
        return self._llm

    async def generate_response(self, prompt: str) -> dict:
        try:
            logger.info("generating_response", model=self.model_name, provider="groq")
            response = await self.llm.ainvoke(prompt)
            
            content = response.content
            usage_metadata = response.response_metadata.get("token_usage", {})
            
            # Extract actual token counts from standard OpenAI response struct
            prompt_tokens = usage_metadata.get("prompt_tokens", 0)
            candidates_token_count = usage_metadata.get("completion_tokens", 0)
            
            # Fallback estimation if usage isn't returned
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
            logger.error("groq_generation_failed", error=str(e))
            raise e

groq_client = GroqClient()
