from langchain_core.prompts import PromptTemplate

RAG_PROMPT = PromptTemplate.from_template(
    """
    Tu es un assistant IA professionnel.

    Réponds uniquement à partir du contexte fourni.
    Si la réponse n'est pas dans le contexte, dis :
    "Je ne trouve pas l'information dans les documents fournis."

    Contexte:
    {context}

    Question:
    {question}

    Réponse claire et professionnelle:
    """
)