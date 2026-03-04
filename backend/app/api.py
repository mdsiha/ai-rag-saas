from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import IndexRequest, ChatRequest, ChatResponse
from app.indexer import index_text
from app.rag_chain import ask_question, stream_answer
from app.security import is_safe_question

router = APIRouter()

@router.post("/index")
def index_document(request: IndexRequest):
    chunks = index_text(request.text)
    return {"message": f"{chunks} chunks indexed successfully."}

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