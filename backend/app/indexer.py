from app.document_loader import load_text, split_documents
from app.vector_store import get_vector_store

def index_text(text: str):
    docs = load_text(text)
    chunks = split_documents(docs)

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    return len(chunks)