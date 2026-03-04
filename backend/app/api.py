from fastapi import APIRouter
from app.schemas import IndexRequest, ChatRequest, ChatResponse
from app.indexer import index_text
from app.rag_chain import ask_question

router = APIRouter()

@router.post("/index")
def index_document(request: IndexRequest):
    chunks = index_text(request.text)
    return {"message": f"{chunks} chunks indexed successfully."}

@router.post("/chat")
def chat(request: ChatRequest):
    answer = ask_question(request.question)
    return ChatResponse(answer=answer)