from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import shutil
import os
from app.schemas import ChatRequest, ChatResponse
from app.indexer import index_pdf_file
from app.rag_chain import ask_question, stream_answer
from app.security import is_safe_question
from app.logger import logger

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB limit

@router.post("/chat")
def chat(request: ChatRequest):
    if not is_safe_question(request.question):
        raise HTTPException(status_code=400, detail="Query is not safe.")
    
    answer = ask_question(request.question)
    return ChatResponse(answer=answer)

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    if not is_safe_question(request.question):
        raise HTTPException(status_code=400, detail="Query is not safe.")

    def generate():
        for chunk in stream_answer(request.question):
            yield f"data: {chunk}\n\n"
        
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    logger.info(f"Processing upload for: {file.filename}")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid format. Only PDF files are allowed.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        logger.warning(f"File {file.filename} exceeds 10MB limit.")
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        num_chunks = index_pdf_file(file_path)
        return {
            "filename": file.filename,
            "status": "success",
            "chunks_indexed": num_chunks,
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Critical error during indexing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the document.")