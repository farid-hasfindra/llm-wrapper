import shutil
import os
import aiofiles
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.api.v1 import chat
from app.rag.ingestion import ingest_docs
from app.core.logging import logger

router = APIRouter()

DOCS_DIR = "data/docs"

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a document (txt) and trigger ingestion in the background.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported for now.")
    
    os.makedirs(DOCS_DIR, exist_ok=True)
    file_path = os.path.join(DOCS_DIR, file.filename)
    
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        logger.info("file_uploaded", filename=file.filename)
        
        # Trigger background ingestion
        background_tasks.add_task(ingest_docs, DOCS_DIR)
        
        return {"message": f"File '{file.filename}' uploaded successfully. Ingestion started in background."}
        
    except Exception as e:
        logger.error("upload_failed", error=str(e))
        raise HTTPException(status_code=500, detail="File upload failed")

@router.delete("/{filename}")
async def delete_document(filename: str):
    """
    Delete a document and re-ingest the remaining documents to update the vector store.
    """
    file_path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(file_path)
        logger.info("file_deleted", filename=filename)
        
        # Re-ingest to update vector store
        # Note: Ideally, we would delete specific vectors, but Chroma/LangChain abstraction 
        # makes full re-ingestion safer for consistency in this simple setup.
        # For production with large datasets, we would need a more granular approach.
        await ingest_docs(DOCS_DIR)
        
        return {"message": f"File '{filename}' deleted and knowledge base updated."}
    except Exception as e:
        logger.error("delete_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Delete failed")

@router.post("/reset")
async def reset_documents():
    """
    Delete all documents and clear the knowledge base.
    """
    try:
        if os.path.exists(DOCS_DIR):
            shutil.rmtree(DOCS_DIR)
            os.makedirs(DOCS_DIR)
        
        # Reset Vector Store (by clearing the persistence directory)
        from app.core.config import settings
        if os.path.exists(settings.VECTOR_STORE_PATH):
            shutil.rmtree(settings.VECTOR_STORE_PATH)
            
        logger.info("knowledge_base_reset")
        return {"message": "All documents deleted and knowledge base reset."}
    except Exception as e:
        logger.error("reset_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Reset failed")
