from pypdf import PdfReader
import os
from sklearn.feature_extraction.text import TfidfVectorizer

_tfidf = None
_documents = {}
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
    global _tfidf
    if not text or len(text.strip()) < 10:
        _documents[session_id] = []
        return
    
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    _documents[session_id] = chunks
    
    try:
        _tfidf = TfidfVectorizer(max_features=100, stop_words='english', min_df=1)
        _tfidf.fit(chunks)
    except:
        _documents[session_id] = []

def get_relevant_chunk(message, session_id):
    if session_id not in _documents or not _documents[session_id]:
        return None
    chunks = _documents[session_id]
    if not chunks or not _tfidf:
        return None
    try:
        scores = _tfidf.transform([message]).toarray()[0]
        best_idx = scores.argmax() if scores.max() > 0 else -1
        return chunks[best_idx] if best_idx >= 0 else None
    except:
        return None
