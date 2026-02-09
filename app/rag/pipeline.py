from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.llm.gemini_client import gemini_client
from app.rag.retriever import get_retriever
from app.core.logging import logger

# Default RAG Prompt
RAG_TEMPLATE = """Answer the question based only on the following context:
{context}

Question: {question}
"""

def get_rag_chain():
    """
    Constructs the RAG chain.
    """
    retriever = get_retriever()
    llm = gemini_client.llm
    
    prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

async def generate_rag_response(question: str) -> str:
    """
    Generates a response using the RAG pipeline.
    """
    try:
        chain = get_rag_chain()
        logger.info("generating_rag_response", question=question)
        response = await chain.ainvoke(question)
        return response
    except Exception as e:
        logger.error("rag_generation_failed", error=str(e))
        raise e
