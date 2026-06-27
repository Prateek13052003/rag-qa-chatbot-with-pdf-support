from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from dotenv import load_dotenv
from utils import load_pdf, create_vectorstore, chat_with_rag, get_chat_history

load_dotenv()

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Server running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), session_id: str = Form(...)):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        documents = load_pdf(temp_path)
        create_vectorstore(documents, session_id)
        os.remove(temp_path)
        
        return {"message": f"PDF loaded: {file.filename}", "pages": len(documents), "session_id": session_id}
    except Exception as e:
        return {"error": str(e)}, 400

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = await chat_with_rag(request.message, request.session_id)
        return result
    except Exception as e:
        return {"error": str(e)}, 400

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    history = get_chat_history(session_id)
    return {"messages": [{"role": m.type, "content": m.content} for m in history.messages]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
