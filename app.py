import os
import streamlit as st
from dotenv import load_dotenv

# LangChain Community Components
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders.pdf import PyPDFLoader

# Embeddings (ONLY OpenAI — works on Python 3.9)
from langchain_openai import OpenAIEmbeddings

# LangChain Core Components
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Groq LLM (correct for langchain-groq==0.3.8)
from langchain_groq import ChatGroq

load_dotenv()

st.title("📄 Chat with your PDF (Stable for Python 3.9 + LC 0.3.27)")
st.write("RAG + Chat History using OpenAI embeddings + Groq LLM.")

# ----------------------------
# Enter API keys
# ----------------------------
openai_key = st.text_input("Enter OpenAI API key:", type="password")
groq_key = st.text_input("Enter Groq API key:", type="password")

llm = None
if groq_key:
    llm = ChatGroq(
        groq_api_key=groq_key,
        model_name="llama-3.1-8b-instant"
    )

# ----------------------------
# Embeddings (OpenAI ONLY)
# ----------------------------
if openai_key:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=openai_key
    )
else:
    embeddings = None

# ----------------------------
# Session Memory
# ----------------------------
session_id = st.text_input("Session ID:", value="default_session")

if "memory" not in st.session_state:
    st.session_state["memory"] = {}

def get_session_history(sid):
    if sid not in st.session_state["memory"]:
        st.session_state["memory"][sid] = ChatMessageHistory()
    return st.session_state["memory"][sid]

# ----------------------------
# Upload PDFs
# ----------------------------
uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
documents = []

if uploaded_files:
    for uf in uploaded_files:
        temp_path = f"temp_{uf.name}"
        with open(temp_path, "wb") as f:
            f.write(uf.getvalue())
        loader = PyPDFLoader(temp_path)
        documents.extend(loader.load())

# ----------------------------
# Build Vectorstore
# ----------------------------

retriever = None

if documents and embeddings:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(splits, embeddings)
    retriever = vectorstore.as_retriever()

# ----------------------------
# Prompts
# ----------------------------

contextual_prompt = ChatPromptTemplate.from_messages([
    ("system", "Rewrite the user's question into a standalone question."),
    MessagesPlaceholder("chat_history"),
    ("user", "{input}")
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Answer the user's question using ONLY the provided context. "
     "If the answer isn't in the context, say 'I don't know'."),
    MessagesPlaceholder("chat_history"),
    ("user", "{input}"),
    ("system", "Context:\n\n{context}")
])

# ----------------------------
# Manual RAG pipeline
# ----------------------------

def run_rag(user_text, history):
    # 1. Reformulate question
    reform_msg = contextual_prompt.format_messages(
        input=user_text,
        chat_history=history.messages
    )
    reformulated = llm.invoke(reform_msg).content

    # 2. Retrieve
    ctx_docs = retriever.invoke(reformulated)
    context = "\n\n".join([d.page_content for d in ctx_docs])

    # 3. Answer
    answer_msg = qa_prompt.format_messages(
        input=user_text,
        context=context,
        chat_history=history.messages
    )
    answer = llm.invoke(answer_msg).content

    return answer

# ----------------------------
# Chat interaction
# ----------------------------

user_input = st.text_input("Ask a question:")

if user_input:
    if embeddings is None:
        st.warning("Enter your OpenAI Embeddings API key.")
    elif retriever is None:
        st.warning("Upload PDFs first.")
    elif llm is None:
        st.warning("Enter your Groq API key.")
    else:
        history = get_session_history(session_id)
        answer = run_rag(user_input, history)

        # Save in chat history
        history.add_user_message(user_input)
        history.add_ai_message(answer)

        st.write("### Answer:")
        st.info(answer)
