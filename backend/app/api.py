from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import shutil
import os
from app.schemas import ChatRequest, ChatResponse
from app.indexer import index_pdf_file
from app.rag_chain import ask_question, stream_answer
from app.security import is_safe_question

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/chat")
def chat(request: ChatRequest):
    if not is_safe_question(request.question):
        raise HTTPException(status_code=400, detail="Requête non sécurisée détectée.")
    
    answer = ask_question(request.question)
    return ChatResponse(answer=answer)

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    if not is_safe_question(request.question):
        raise HTTPException(status_code=400, detail="Requête non sécurisée détectée.")

    def generate():
        for chunk in stream_answer(request.question):
            yield chunk
        
    return StreamingResponse(generate(), media_type="text/plain")

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
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