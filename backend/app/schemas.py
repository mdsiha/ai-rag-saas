from pydantic import BaseModel

class IndexRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str