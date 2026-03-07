from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

_embeddings_instance = None

def get_embeddings():
    """Returns the Google Generative AI Embeddings model as a singleton."""
    global _embeddings_instance
    if _embeddings_instance is not None:
        return _embeddings_instance

    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set")
    
    _embeddings_instance = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.GOOGLE_API_KEY
    )
    return _embeddings_instance
