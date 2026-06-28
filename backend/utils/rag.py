import chromadb
from pypdf import PdfReader
import os
from sentence_transformers import SentenceTransformer

# Lazy load - only when needed
_embeddings_model = None
chroma_client = chromadb.EphemeralClient()
_groq_client = None

def get_embeddings_model():
    global _embeddings_model
    if _embeddings_model is None:
        _embeddings_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embeddings_model

def get_groq_client():
    global _groq_client
    if _groq_client is None:
        import groq
        _groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _groq_client

def load_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def create_vectorstore(text, session_id):
    embeddings_model = get_embeddings_model()
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    embeddings = [embeddings_model.encode(chunk).tolist() for chunk in chunks]
    collection = chroma_client.get_or_create_collection(name=f"session_{session_id}")
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=chunks
    )

def get_vectorstore(session_id):
    return chroma_client.get_or_create_collection(name=f"session_{session_id}")
