from pydantic import BaseModel, EmailStr
from typing import Optional

class ChatRequest(BaseModel):
    question: str
    file_filter: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str

# Authentication

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True