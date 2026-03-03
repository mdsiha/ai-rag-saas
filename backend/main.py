from app.document_loader import load_text, split_documents
from app.llm import get_llm
from app.prompts import RAG_PROMPT
from app.vector_store import get_vector_store

def test_llm():
    llm = get_llm()

    prompt = RAG_PROMPT.format(
        context="Un RAG est un système qui combine recherche documentaire et LLM.",
        question="Qu'est-ce qu'un RAG ?"
    )

    response = llm.invoke(prompt)

    print("\n=== RESPONSE ===\n")
    print(response)

def test_vector_store():
    text = """
    Le RAG (Retrieval Augmented Generation) est une architecture
    combinant recherche documentaire et modèles de langage.
    Il permet de réduire les hallucinations.
    """

    docs = load_text(text)
    chunks = split_documents(docs)

    vector_store = get_vector_store()

    vector_store.add_documents(chunks)

    results = vector_store.similarity_search("Comment réduire les hallucinations ?", k=2)

    print("\n=== RESULTS ===\n")

    for r in results:
        print(r.page_content)
        print("------")

if __name__ == "__main__":
    #test_llm()
    test_vector_store()