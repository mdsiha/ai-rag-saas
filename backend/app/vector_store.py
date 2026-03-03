from langchain_chroma import Chroma
from .embeddings import get_embeddings

PERSIST_DIRECTORY = "chroma_db"

def get_vector_store():
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )