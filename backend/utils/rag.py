import chromadb
from pypdf import PdfReader
import os
from sentence_transformers import SentenceTransformer

# Initialize embeddings
embeddings_model = SentenceTransformer("all-MiniLM-L6-v2")

# New Chroma client (v0.4+)
chroma_client = chromadb.EphemeralClient()

# Clients initialized lazily
_groq_client = None

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
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    embeddings = [embeddings_model.encode(chunk).tolist() for chunk in chunks]
    collection = chroma_client.get_or_create_collection(name=f"session_{session_id}")
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=chunks
    )
    print("COLLECTION COUNT:", collection.count())

def get_vectorstore(session_id):
    return chroma_client.get_or_create_collection(name=f"session_{session_id}")
