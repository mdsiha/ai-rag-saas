import os
from app.document_loader import load_pdf, split_documents
from app.vector_store import get_vector_store

def index_pdf_file(file_path: str):
    docs = load_pdf(file_path)
    
    chunks = split_documents(docs)

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    return len(chunks)