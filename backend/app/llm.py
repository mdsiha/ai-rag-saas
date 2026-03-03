from langchain_ollama import OllamaLLM
from .config import MODEL_NAME, TEMPERATURE

def get_llm():
    return OllamaLLM(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )