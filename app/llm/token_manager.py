from dataclasses import dataclass
from typing import Optional

# Pricing for Gemini 1.5 Flash (Example rates, update as needed)
# PER 1M TOKENS
INPUT_PRICE_PER_1M = 0.35
OUTPUT_PRICE_PER_1M = 0.70

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float

class TokenManager:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Calculate estimated cost in USD based on token usage.
        """
        input_cost = (prompt_tokens / 1_000_000) * INPUT_PRICE_PER_1M
        output_cost = (completion_tokens / 1_000_000) * OUTPUT_PRICE_PER_1M
        return round(input_cost + output_cost, 6)

    def estimate_tokens(self, text: str) -> int:
        """
        Rough estimation of tokens (char count / 4).
        For production, use google.generativeai.count_tokens if available,
        or a proper tokenizer.
        """
        return len(text) // 4

    def create_usage_report(self, prompt_tokens: int, completion_tokens: int) -> TokenUsage:
        cost = self.calculate_cost(prompt_tokens, completion_tokens)
        return TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            estimated_cost=cost
        )

token_manager = TokenManager()
