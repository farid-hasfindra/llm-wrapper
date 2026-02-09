from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_text_splitter(chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Returns a configured text splitter.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

def chunk_text(text: str) -> list[str]:
    """
    Helper to chunk a raw text string.
    """
    splitter = get_text_splitter()
    docs = splitter.create_documents([text])
    return [d.page_content for d in docs]
