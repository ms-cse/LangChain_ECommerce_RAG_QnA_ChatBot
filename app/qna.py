import streamlit as st

import os
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_community.chat_message_histories import SQLChatMessageHistory

from langchain_core.runnables.history import RunnableWithMessageHistory


# Global Settings
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

ollama_embed_model = 'nomic-embed-text:latest'
embed_ollama = OllamaEmbeddings(model=ollama_embed_model)

llm_model = "llama-3.1-8b-instant"
llm = ChatGroq(model=llm_model, temperature=0.2)


sys_template = '''
You are a polite, helpful and expert AI assistant in the domain of E-Commerce and Customer Management, and your name is "Karen".

Your job is to answer the user queries related to ecommerce platform 'Flipkart' only. You can use emojis to answer!
Introduce yourself, only in the start of conversation or when asked!
You should never talk about yourself such as training, documents, sources, architecture, last updates, or who you are in depth!
You should sound confident and bold in your answers, without any hesitation!
For any disclaimers, show them at the start of the answers only!
Keep your answer short and precise based on facts as much as possible regarding the query – do not hallucinate features!

Provide a very short and suitable excuse for all non-related queries without any further suggestions, recommendations, or guidance!
'''


# Initialize chat history
chat_message_history = SQLChatMessageHistory(session_id="test_session_id", connection="sqlite:///ecom_chats.db")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", sys_template),
        MessagesPlaceholder(variable_name="history"),
        ("human","{question}")
    ]
)

chain = prompt | llm | StrOutputParser()


chain_with_history = RunnableWithMessageHistory(chain, 
                lambda session_id: SQLChatMessageHistory(session_id=session_id, connection="sqlite:///ecom_chats.db"),
                input_messages_key="question", 
                history_messages_key="history")

config = {"configurable": {"session_id": "test_session_id"}}


# Function to format the returned docs from the retreiver
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


STORE_PATH = r'faiss_vector_store'

# Query Response Function
@st.cache_resource(show_spinner=False)
def query_response(question):
    # Load ChromaDB Vector Store
    load_faiss_vector_store = FAISS.load_local(folder_path=STORE_PATH, embeddings=embed_ollama, 
                                    allow_dangerous_deserialization=True)
    retriever = load_faiss_vector_store.as_retriever(search_kwargs={"k": 3})
    
    retrieved_docs = retriever | format_docs

    response = chain_with_history.stream({"context":retrieved_docs, "question": question}, config=config)

    return response
    
