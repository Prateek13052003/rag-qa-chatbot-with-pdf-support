chat_histories = {}

def get_chat_history(session_id):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

async def chat_with_rag(message: str, session_id: str):
    history = get_chat_history(session_id)
    history.append({"role": "user", "content": message})
    answer = f"Test response: You asked '{message}'"
    history.append({"role": "ai", "content": answer})
    return {"answer": answer, "source": "test"}
