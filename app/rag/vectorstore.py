import os
from langchain_community.vectorstores import Chroma
from app.core.config import settings
from app.rag.embeddings import get_embeddings
from app.core.logging import logger

_vectorstore_cache = {}

def get_vectorstore(user_id: str = "guest"):
    """
    Initializes and returns the Chroma vector store for a specific user, using an in-memory dictionary cache.
    """
    global _vectorstore_cache
    if user_id in _vectorstore_cache:
        return _vectorstore_cache[user_id]

    embeddings = get_embeddings()
    
    # Isolate storage per user
    user_persist_dir = os.path.join(settings.VECTOR_STORE_PATH, user_id)
    os.makedirs(user_persist_dir, exist_ok=True)
    
    try:
        vectorstore = Chroma(
            persist_directory=user_persist_dir,
            embedding_function=embeddings
        )
        _vectorstore_cache[user_id] = vectorstore
        return vectorstore
    except Exception as e:
        logger.error("failed_to_init_vectorstore", error=str(e), user_id=user_id)
        raise e
