import os
from langchain_chroma import Chroma
from .embeddings import get_embeddings

PERSIST_DIRECTORY = "chroma_db"

def get_vector_store():
    if not os.path.exists(PERSIST_DIRECTORY):
        os.makedirs(PERSIST_DIRECTORY)
        
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )