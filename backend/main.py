from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from dotenv import load_dotenv
import traceback

load_dotenv()
app = FastAPI(title="RAG Chatbot API", version="1.0.0")

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
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), session_id: str = Form(...)):
    try:
        from utils import load_pdf, create_vectorstore
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        documents = load_pdf(temp_path)
        create_vectorstore(documents, session_id)
        os.remove(temp_path)
        return {"message": f"PDF loaded: {file.filename}", "status": "success"}
    except Exception as e:
        print(f"UPLOAD ERROR: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        from utils.chat_service import chat_with_rag
        result = await chat_with_rag(request.message, request.session_id)
        return result
    except Exception as e:
        print(f"CHAT ERROR: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
