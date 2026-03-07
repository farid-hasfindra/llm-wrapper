from app.rag.vectorstore import get_vectorstore

def get_retriever(k: int = 4, user_id: str = "guest"):
    """
    Returns a retriever from the vector store for a specific user.
    """
    vectorstore = get_vectorstore(user_id=user_id)
    return vectorstore.as_retriever(search_kwargs={"k": k})
