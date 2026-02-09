import os
from langchain_community.vectorstores import Chroma
from app.core.config import settings
from app.rag.embeddings import get_embeddings
from app.core.logging import logger

def get_vectorstore():
    """
    Initializes and returns the Chroma vector store.
    """
    embeddings = get_embeddings()
    
    # Ensure directory exists
    os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)
    
    try:
        vectorstore = Chroma(
            persist_directory=settings.VECTOR_STORE_PATH,
            embedding_function=embeddings
        )
        return vectorstore
    except Exception as e:
        logger.error("failed_to_init_vectorstore", error=str(e))
        raise e
