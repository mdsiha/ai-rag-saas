from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_text(text: str):
    return [Document(page_content=text)]

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    return splitter.split_documents(documents)