import os
from .rag import get_groq_client

chat_histories = {}

def get_chat_history(session_id):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

async def chat_with_rag(message: str, session_id: str):
    history = get_chat_history(session_id)
    
    try:
        groq_client = get_groq_client()
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": message}],
            max_tokens=500,
            temperature=0.7
        )
        answer = response.choices[0].message.content
        history.append({"role": "user", "content": message})
        history.append({"role": "ai", "content": answer})
        return {"answer": answer, "source": "groq"}
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "ai", "content": error_msg})
        return {"answer": error_msg, "source": "error"}
