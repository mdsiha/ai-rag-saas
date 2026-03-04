from app.indexer import index_text
from app.rag_chain import ask_question

def main():
    print("Indexation document...")
    index_text("""
    Le RAG (Retrieval Augmented Generation) est une architecture
    combinant recherche documentaire et modèles de langage.
    Il permet de réduire les hallucinations en injectant du contexte pertinent.
    """)

    print("Document indexé !")

    question = input("\nPose ta question : ")

    answer = ask_question(question)

    print("\n=== ANSWER ===\n")
    print(answer)

if __name__ == "__main__":
    main()