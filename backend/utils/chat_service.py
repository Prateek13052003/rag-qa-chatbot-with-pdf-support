chat_histories = {}

def get_chat_history(session_id):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

async def chat_with_rag(message: str, session_id: str):
    from .rag import get_groq_client
    
    history = get_chat_history(session_id)
    groq_client = get_groq_client()
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # ✅ UPDATED MODEL
            messages=[{"role": "user", "content": message}],
            max_tokens=500
        )
        answer = response.choices[0].message.content
        history.append({"role": "user", "content": message})
        history.append({"role": "ai", "content": answer})
        return {"answer": answer, "source": "llm"}
    except Exception as e:
        raise Exception(f"Chat error: {str(e)}")
