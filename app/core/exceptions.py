class LLMWrapperException(Exception):
    """Base exception for LLM Wrapper"""
    pass

class ConfigurationError(LLMWrapperException):
    """Configuration related errors"""
    pass

class LLMProviderError(LLMWrapperException):
    """Errors related to LLM provider (Gemini) interactions"""
    pass
