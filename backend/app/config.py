import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "AI RAG SaaS"
    VERSION: str = "1.0.0"

    # Cors Settings
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return v

    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # AI Providers
    AI_PROVIDER: str = "groq"
    
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4o"
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"

    # Database & Server
    PERSIST_DIRECTORY: str = "chroma_db"
    TEMPERATURE: float = 0.2
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Pydantic Settings
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()