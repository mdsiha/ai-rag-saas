from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from app.vector_store import get_vector_store
from app.llm import get_llm

# Ephemeral history (replace with Redis or DB for production)
chat_histories = {}

def get_session_history(session_id: str):
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

def create_conversational_rag_chain():
    llm_instance = get_llm()
    
    system_prompt = (
        "You are a professional AI assistant. Answer strictly based on the provided context. "
        "If you do not know the answer, state that you cannot find the information in the documents.\n\n"
        "Context:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    # 1. Synthesis chain
    question_answer_chain = create_stuff_documents_chain(llm_instance, prompt)
    
    # 2. Vector database link
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    
    retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)

    # 3. Add history management
    return RunnableWithMessageHistory(
        retrieval_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

# Chain singleton
conversational_rag_chain = create_conversational_rag_chain()

def ask_question(question: str):
    response = conversational_rag_chain.invoke(
        {"input": question},
        config={"configurable": {"session_id": "default"}}
    )
    return response["answer"]

def stream_answer(question: str):
    for chunk in conversational_rag_chain.stream(
        {"input": question},
        config={"configurable": {"session_id": "default"}}
    ):
        answer_chunk = chunk.get("answer")
        if answer_chunk:
            yield answer_chunk