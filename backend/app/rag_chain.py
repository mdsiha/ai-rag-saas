from app.vector_store import get_vector_store
from app.llm import get_llm
from app.prompts import RAG_PROMPT
from app.security import is_safe_question

def ask_question(question: str):
    # Security
    if not is_safe_question(question):
        return "Votre question contient un contenu non autorisé."

    # Get vector store
    vector_store = get_vector_store()

    # Get similar documents
    results = vector_store.similarity_search(question, k=3)

    # No results
    if not results:
        return "Je ne trouve pas l'information dans les documents fournis."

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