class WindowManager:
    """
    Manages the sliding window of context.
    """
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    def trim_history(self, history: list) -> list:
        # Simple implementation: keep last N messages
        return history[-10:]
