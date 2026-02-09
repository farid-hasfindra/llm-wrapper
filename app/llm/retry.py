import asyncio
from typing import Callable, Any
from app.core.logging import logger

class RetryHandler:
    """
    Handles exponential backoff and retry logic for external API calls.
    """
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        attempt = 0
        last_exception = None

        while attempt < self.max_retries:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                attempt += 1
                last_exception = e
                wait_time = self.base_delay * (2 ** (attempt - 1))
                logger.warning("retry_attempt", attempt=attempt, error=str(e), wait_time=wait_time)
                await asyncio.sleep(wait_time)
        
        logger.error("max_retries_exceeded", error=str(last_exception))
        raise last_exception
