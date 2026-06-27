# RAG Chatbot Setup Guide

## Prerequisites
- Python 3.9+
- Node.js 16+
- Groq API Key (free)
- Google Gemini API Key (free - fallback)
- Serper API Key (free tier available - web search)

## Backend Setup

1. Create `.env` file in `backend/`:
```bash
cp backend/.env.example backend/.env
```

2. Add your API keys to `backend/.env`:
3. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Run server:
```bash
python main.py
```
Server runs on `http://localhost:8000`

## Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run dev server:
```bash
npm run dev
```
Frontend runs on `http://localhost:3000`

## Testing
- Upload a PDF
- Ask questions
- System will check PDF first, then web search, then LLM

## Deployment
See DEPLOY.md
