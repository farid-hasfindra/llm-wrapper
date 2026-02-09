import pytest
from app.rag.chunking import get_text_splitter

def test_chunking():
    text = "A" * 2000
    splitter = get_text_splitter(chunk_size=1000, chunk_overlap=0)
    chunks = splitter.create_documents([text])
    assert len(chunks) >= 2
    assert len(chunks[0].page_content) <= 1000
