import asyncio
import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.rag.ingestion import ingest_docs
from app.core.logging import setup_logging

setup_logging()

if __name__ == "__main__":
    asyncio.run(ingest_docs())
