from app.document_loader import load_text, split_documents
from app.vector_store import get_vector_store
from app.rag_chain import ask_question

def setup_demo_data():
    text = """
    Le RAG (Retrieval Augmented Generation) est une architecture
    combinant recherche documentaire et modèles de langage.
    Il permet de réduire les hallucinations en injectant du contexte pertinent.
    """

    docs = load_text(text)
    chunks = split_documents(docs)

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

def test_rag():
    question = "Comment le RAG reduit-il les hallucinations ?"

    answer = ask_question(question)

    print("\n=== QUESTION ===\n")
    print(question)

    print("\n=== ANSWER ===\n")
    print(answer)

if __name__ == "__main__":
    setup_demo_data()
    test_rag()