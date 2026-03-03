from app.llm import get_llm
from app.prompts import RAG_PROMPT

def test_llm():
    llm = get_llm()

    prompt = RAG_PROMPT.format(
        context="Un RAG est un système qui combine recherche documentaire et LLM.",
        question="Qu'est-ce qu'un RAG ?"
    )

    response = llm.invoke(prompt)

    print("\n=== RESPONSE ===\n")
    print(response)

if __name__ == "__main__":
    test_llm()