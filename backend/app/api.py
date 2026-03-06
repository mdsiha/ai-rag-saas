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

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10Mo

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
    logger.info(f"Received file: {file.filename}")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        logger.warning(f"File {file.filename} is too large.")
        raise HTTPException(status_code=413, detail="File is too large.")

    await file.seek(0)

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        num_chunks = index_pdf_file(file_path)
        return {
            "filename": file.filename,
            "status": "success",
            "chunks_indexed": num_chunks,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error indexing file : {str(e)}")