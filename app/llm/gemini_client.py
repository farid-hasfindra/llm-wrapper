import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.core.logging import logger

class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7):
        if not settings.GOOGLE_API_KEY:
            logger.warning("GOOGLE_API_KEY not set. Gemini features will not work.")
        
        genai.configure(api_key=settings.GOOGLE_API_KEY)
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

    async def generate_response(self, prompt: str) -> str:
        try:
            logger.info("generating_response", model=self.model_name)
            response = await self.llm.ainvoke(prompt)
            return response.content
        except Exception as e:
            logger.error("gemini_generation_failed", error=str(e))
            raise e

gemini_client = GeminiClient()
