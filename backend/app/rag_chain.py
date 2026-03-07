from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from app.vector_store import get_vector_store
from app.llm import llm

system_prompt = (
    "Tu es un assistant IA professionnel. Réponds uniquement à partir du contexte fourni. "
    "Si tu ne sais pas, dis que tu ne trouves pas l'information.\n\n"
    "Context:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)

vector_store = get_vector_store()
retrieval_chain = create_retrieval_chain(vector_store.as_retriever(), question_answer_chain)

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

def get_session_history(session_id: str):
    return demo_ephemeral_chat_history_for_chain

conversational_rag_chain = RunnableWithMessageHistory(
    retrieval_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

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