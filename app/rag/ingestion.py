import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.vectorstore import get_vectorstore
from app.core.logging import logger

async def ingest_docs(docs_path: str = "data/docs"):
    """
    Ingests documents from a directory into the vector store.
    """
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
        logger.warning(f"Created {docs_path}. Please add text files there to ingest.")
        return

    logger.info("loading_documents", path=docs_path)
    # Load documents
    # Note: DirectoryLoader with glob="**/*.txt" currently only loads .txt files.
    # You can extend this to load .pdf, .docx, etc.
    loader = DirectoryLoader(docs_path, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        logger.warning("no_documents_found")
        return

    logger.info("splitting_documents", count=len(documents))
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    
    logger.info("embedding_documents", chunk_count=len(texts))
    # Create/Update Vector Store
    vectorstore = get_vectorstore()
    vectorstore.add_documents(texts)
    
    logger.info("ingestion_complete")
