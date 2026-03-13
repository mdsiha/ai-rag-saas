from app.vector_store import get_vector_store
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
import shutil
import os
from app.schemas import ChatRequest, ChatResponse
from app.indexer import index_pdf_file
from app.rag_chain import ask_question, stream_answer
from app.security import is_safe_question, get_current_user
from app.database import User
from app.logger import logger

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@router.get("/stats")
async def get_user_stats(current_user: User = Depends(get_current_user)):
    try:
        vector_store = get_vector_store()
        results = vector_store.get(where={"user_id": current_user.id})

        filenames = sorted(list(set([m.get("source", "Inconnu") for m in results["metadatas"]])))

        return {
            "total_chunks": len(results["ids"]),
            "files": filenames
        }
    except Exception as e:
        return {"total_chunks": 0, "files": []}

@router.post("/chat")
def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    if not is_safe_question(request.question):
        raise HTTPException(status_code=400, detail="Security violation: unsafe query detected.")
    
    try:
        answer = ask_question(request.question, user_id=current_user.id, filter_filter=request.file_filter)
        return ChatResponse(answer=answer)
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail="The AI failed to respond. Please check LLM connectivity.")

@router.post("/chat/stream")
def chat_stream(request: ChatRequest, current_user: User = Depends(get_current_user)):
    if not is_safe_question(request.question):
        raise HTTPException(status_code=400, detail="Security violation: unsafe query detected.")

    def generate():
        try:
            for chunk in stream_answer(request.question, user_id=current_user.id, filter_filter=request.file_filter):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            logger.error(f"Stream Error: {e}")
            yield f"data: [SERVER_ERROR]\n\n"
        
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    logger.info(f"Upload received: {file.filename}")

    user_upload_dir = os.path.join(UPLOAD_DIR, f"user_{current_user.id}")
    os.makedirs(user_upload_dir, exist_ok=True)

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid format. Only PDF files are allowed.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        num_chunks = index_pdf_file(file_path, user_id=current_user.id)
        return {
            "filename": file.filename,
            "status": "success",
            "chunks_indexed": num_chunks,
        }
    except Exception as e:
        logger.error(f"Indexing Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))