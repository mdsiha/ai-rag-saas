from app.document_loader import load_pdf, split_documents
from app.vector_store import get_vector_store
from app.logger import logger

def index_pdf_file(file_path: str):
    docs = load_pdf(file_path)

    if not docs or len(docs) == 0:
        raise Exception("The PDF is empty or contains only images (OCR required).")
    
    chunks = split_documents(docs)

    if not chunks or len(chunks) == 0:
        raise Exception("Unable to extract text segments.")

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    logger.info(f"Indexing successful: {len(chunks)} chunks added to the knowledge base.")
    return len(chunks)