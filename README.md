# 🚀 RAG Chatbot with Web Search Fallback 

A production-ready RAG (Retrieval-Augmented Generation) chatbot that combines PDF knowledge with real-time web search.

## ✨ Features

- 📄 **PDF Upload & Processing** - Upload PDFs and chat with their content
- 🌐 **Web Search Fallback** - If answer not in PDF, searches the web
- 🔄 **Multi-LLM Support** - Groq (primary) + Google Gemini (fallback)
- 💬 **Chat History** - Per-session conversation memory
- 🎨 **Beautiful UI** - Modern React/Next.js frontend with Tailwind CSS
- 🔌 **API-First** - FastAPI backend for scalability
- 🚀 **Production Ready** - Easy deployment on Render + Vercel

## 🛠 Tech Stack

**Backend:**
- FastAPI
- LangChain + Groq + Google Gemini
- Chroma (vector DB)
- Serper (web search)
- HuggingFace Embeddings (free)

**Frontend:**
- Next.js 14
- React 18
- Tailwind CSS
- Lucide Icons

## 📋 Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your API keys
python main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`

## 🎯 API Endpoints

- `POST /upload` - Upload PDF
- `POST /chat` - Send message
- `GET /history/{session_id}` - Get chat history
- `GET /health` - Server status

## 📦 Free API Keys

- **Groq**: https://console.groq.com
- **Google Gemini**: https://makersuite.google.com
- **Serper**: https://serper.dev (free tier)

## 🚢 Deploy

See `DEPLOY.md` for step-by-step deployment instructions.

## 📝 License

MIT
