from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI

from app.config import settings
from app.logger import logger

def get_llm():
    """
    Factory to retrieve the configured LLM.
    This approach allows easy switching between providers without refactoring.
    """
    provider = settings.AI_PROVIDER.lower()

    try:
        if provider == "groq":
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY missing in .env")
            logger.info(f"LLM Engine: Groq ({settings.GROQ_MODEL})")
            return ChatGroq(
                model=settings.GROQ_MODEL,
                api_key=settings.GROQ_API_KEY,
                temperature=settings.TEMPERATURE
            )

        elif provider == "azure":
            if not settings.AZURE_OPENAI_API_KEY:
                raise ValueError("AZURE_OPENAI_API_KEY missing")
            logger.info(f"LLM Engine: Azure OpenAI ({settings.AZURE_OPENAI_DEPLOYMENT})")
            return AzureChatOpenAI(
                azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_version="2024-02-15-preview",
                temperature=settings.TEMPERATURE
            )
        else:
            raise ValueError(f"Unsupported AI_PROVIDER: {provider}")

    except Exception as e:
        logger.error(f"Failed to initialize LLM provider {provider}: {e}")
        raise e