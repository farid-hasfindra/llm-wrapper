from dataclasses import dataclass

@dataclass
class CostEstimate:
    total_cost: float
    currency: str = "USD"

class CostEstimator:
    """
    Advanced cost estimation logic.
    Can be extended to support multiple models, dynamic pricing, and user budgets.
    """
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        # Prices per 1M tokens
        self.pricing = {
            "gemini-1.5-flash": {"input": 0.35, "output": 0.70},
            "gemini-1.5-pro": {"input": 3.50, "output": 10.50},
        }

    def estimate(self, prompt_tokens: int, completion_tokens: int) -> CostEstimate:
        rates = self.pricing.get(self.model_name, self.pricing["gemini-1.5-flash"])
        
        input_cost = (prompt_tokens / 1_000_000) * rates["input"]
        output_cost = (completion_tokens / 1_000_000) * rates["output"]
        
        return CostEstimate(total_cost=round(input_cost + output_cost, 6))
