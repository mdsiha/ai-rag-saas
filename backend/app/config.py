from app.vector_store import PERSIST_DIRECTORY
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Provider choice: "groq", "azure"
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "groq")

    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    # Common Parameters
    TEMPERATURE: float = 0.2
    PERSIST_DIRECTORY: str = "chroma_db"

    # Server Settings
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    class Config:
        env_file = ".env"
        extra="ignore"

settings = Settings()