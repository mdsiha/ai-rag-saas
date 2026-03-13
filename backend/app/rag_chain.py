from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from app.vector_store import get_vector_store
from app.llm import get_llm
from app.logger import logger

_chain = None

chat_histories = {}

def get_session_history(session_id: str):
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

def get_conversational_chain():
    global _chain
    if _chain is None:
        logger.info("Initializing RAG Chain (this might take a moment the first time)...")
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

        question_answer_chain = create_stuff_documents_chain(llm_instance, prompt)
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
        retrieval_chain = create_retrieval_chain(retriever, question_answer_chain)

        _chain = RunnableWithMessageHistory(
            retrieval_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
    return _chain

def ask_question(question: str, user_id: int):
    chain = get_conversational_chain()
    response = chain.invoke(
        {"input": question},
        config={
            "configurable": {"session_id": f"user_{user_id}"},
            "search_kwargs": {"filter": {"user_id": user_id}}
        }
    )
    return response["answer"]

def stream_answer(question: str, user_id: int):
    chain = get_conversational_chain()
    for chunk in chain.stream(
        {"input": question},
        config={
            "configurable": {"session_id": f"user_{user_id}"},
            "search_kwargs": {"filter": {"user_id": user_id}}
        }
    ):
        answer_chunk = chunk.get("answer")
        if answer_chunk:
            yield answer_chunk