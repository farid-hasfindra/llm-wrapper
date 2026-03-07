import shutil
import os
import aiofiles
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Header
from app.api.v1 import chat
from app.rag.ingestion import ingest_docs
from app.core.logging import logger

router = APIRouter()

DOCS_DIR = "data/docs"

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    x_user_id: str = Header("guest")
):
    """
    Upload a document (txt) and trigger ingestion in the background for a specific user.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported for now.")
    
    user_docs_dir = os.path.join(DOCS_DIR, x_user_id)
    os.makedirs(user_docs_dir, exist_ok=True)
    file_path = os.path.join(user_docs_dir, file.filename)
    
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        logger.info("file_uploaded", filename=file.filename, user_id=x_user_id)
        
        # Trigger background ingestion
        background_tasks.add_task(ingest_docs, x_user_id, DOCS_DIR)
        
        return {"message": f"File '{file.filename}' uploaded successfully. Ingestion started in background."}
        
    except Exception as e:
        logger.error("upload_failed", error=str(e))
        raise HTTPException(status_code=500, detail="File upload failed")

@router.delete("/{filename}")
async def delete_document(
    filename: str,
    x_user_id: str = Header("guest")
):
    """
    Delete a document and re-ingest the remaining documents to update the user's vector store.
    """
    user_docs_dir = os.path.join(DOCS_DIR, x_user_id)
    file_path = os.path.join(user_docs_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(file_path)
        logger.info("file_deleted", filename=filename, user_id=x_user_id)
        
        # Re-ingest to update vector store
        # Note: Ideally, we would delete specific vectors, but Chroma/LangChain abstraction 
        # makes full re-ingestion safer for consistency in this simple setup.
        # For production with large datasets, we would need a more granular approach.
        await ingest_docs(x_user_id, DOCS_DIR)
        
        return {"message": f"File '{filename}' deleted and knowledge base updated."}
    except Exception as e:
        logger.error("delete_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Delete failed")

@router.post("/reset")
async def reset_documents(x_user_id: str = Header("guest")):
    """
    Delete all documents and clear the knowledge base for a specific user.
    """
    try:
        user_docs_dir = os.path.join(DOCS_DIR, x_user_id)
        if os.path.exists(user_docs_dir):
            shutil.rmtree(user_docs_dir)
            os.makedirs(user_docs_dir)
        
        # Reset Vector Store specifically for this user
        from app.core.config import settings
        user_vector_store_path = os.path.join(settings.VECTOR_STORE_PATH, x_user_id)
        if os.path.exists(user_vector_store_path):
            shutil.rmtree(user_vector_store_path)
            
        logger.info("knowledge_base_reset", user_id=x_user_id)
        return {"message": "All documents deleted and knowledge base reset for user."}
    except Exception as e:
        logger.error("reset_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Reset failed")
