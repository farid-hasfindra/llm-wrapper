from app.rag.vectorstore import get_vectorstore

def get_retriever(k: int = 4):
    """
    Returns a retriever from the vector store.
    """
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(search_kwargs={"k": k})
