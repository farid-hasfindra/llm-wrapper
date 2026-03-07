from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from app.llm.groq_client import groq_client
from app.rag.retriever import get_retriever
from app.core.logging import logger

# Default RAG Prompt definition for a Chat Template
RAG_SYSTEM_TEMPLATE = """You are a helpful AI assistant. Answer the user's question based ONLY on the following context.
If no relevant information is found in the context, you can use your general knowledge, but prioritize the context.

Context:
{context}"""

def get_rag_chain(model: str = None, user_id: str = "guest"):
    """
    Constructs the RAG chain for a specific user, supporting conversation history.
    """
    retriever = get_retriever(user_id=user_id)
    llm = groq_client.get_llm(model)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_TEMPLATE),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        RunnablePassthrough.assign(
            context=(lambda x: x["question"]) | retriever | format_docs
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

async def generate_rag_response(question: str, model: str = None, user_id: str = "guest", chat_history: list = None) -> str:
    """
    Generates a response using the RAG pipeline for a specific user with memory.
    """
    try:
        chain = get_rag_chain(model=model, user_id=user_id)
        
        # Convert Pydantic schemas to Langchain objects
        formatted_history = []
        if chat_history:
            for msg in chat_history:
                if msg.role == 'user':
                    formatted_history.append(HumanMessage(content=msg.content))
                elif msg.role in ['ai', 'assistant']:
                    formatted_history.append(AIMessage(content=msg.content))
                    
        logger.info("generating_rag_response", question=question, model=model, user_id=user_id, has_history=bool(chat_history))
        response = await chain.ainvoke({
            "question": question,
            "chat_history": formatted_history
        })
        return response
    except Exception as e:
        logger.error("rag_generation_failed", error=str(e))
        raise e
