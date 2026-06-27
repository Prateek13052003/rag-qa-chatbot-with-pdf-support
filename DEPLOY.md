# Deployment Guide

## Backend Deployment (Render)

1. Push code to GitHub
2. Go to render.com → New → Web Service
3. Connect GitHub repo
4. Settings:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && python main.py`
   - Environment Variables: Add GROQ_API_KEY, GOOGLE_API_KEY, SERPER_API_KEY
5. Deploy!

Backend URL: `https://your-service.onrender.com`

## Frontend Deployment (Vercel)

1. Go to vercel.com → New Project
2. Import GitHub repo
3. Framework: Next.js (auto-detected)
4. Environment Variables:
   - `NEXT_PUBLIC_API_URL=https://your-service.onrender.com`
5. Deploy!

## Local Testing Before Deploy

### Terminal 1 (Backend):
```bash
cd backend
python main.py
```

### Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000`
