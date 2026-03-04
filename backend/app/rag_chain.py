from app.vector_store import get_vector_store
from app.llm import get_llm
from app.prompts import RAG_PROMPT

def ask_question(question: str):
    # Get vector store
    vector_store = get_vector_store()

    # Get similar documents
    results = vector_store.similarity_search(question, k=3)

    # Create context
    context = "\n\n".join([doc.page_content for doc in results])

    # Create prompt
    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    # Invoke LLM
    llm = get_llm()
    response = llm.invoke(prompt)

    return response