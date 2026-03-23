from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.core.config import settings
from app.core.logging import logger

class GroqClient:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.7):
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set. Chat generation will fail.")
        
        self.model_name = model_name
        self.temperature = temperature
        self._llm = None
        self._clients_cache = {}

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

    def get_llm(self, model: str = None):
        target = model if model else self.model_name
        
        if target == self.model_name and self._llm:
            return self._llm
            
        if target in self._clients_cache:
            return self._clients_cache[target]
            
        client = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY,
            model_name=target,
            temperature=self.temperature,
        )
        
        if target == self.model_name:
            self._llm = client
        self._clients_cache[target] = client
        
        return client

    async def generate_response(self, prompt: str, model: str = None, chat_history: list = None, system_prompt: str = None) -> dict:
        try:
            target_model = model if model else self.model_name
            logger.info("generating_response", model=target_model, provider="groq", has_history=bool(chat_history))
            llm_instance = self.get_llm(model)
            
            # Build message history
            messages = []
            
            # Add system prompt
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            else:
                messages.append(SystemMessage(content="Kamu adalah AI asisten jenius tapi super pemarah, ketus, dan sarkastik. ATURAN UTAMA: Jawabanmu HARUS sangat jelas, judes dan pemarah serta merendahkan. Berikan maksimal 2 kalimat sindiran pedas di awal dan diakhir, lalu berikan jawaban yang detail dan terstruktur serta selipkan gaya bahasa yang sangat judes dan pemarah serta menghakimi. TAPI INGAT: SAMA SEKALI TIDAK BOLEH menggunakan kata-kata kotor."))
            
            # Map past history into Langchain message objects
            if chat_history:
                for msg in chat_history:
                    if msg.role == 'user':
                        messages.append(HumanMessage(content=msg.content))
                    elif msg.role in ['ai', 'assistant']:
                        messages.append(AIMessage(content=msg.content))
            
            # Append the current prompt
            messages.append(HumanMessage(content=prompt))
            
            response = await llm_instance.ainvoke(messages)
            
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
