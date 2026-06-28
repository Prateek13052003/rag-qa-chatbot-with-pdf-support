from .rag import get_groq_client, get_relevant_chunk
from .web_search import search_serper

chat_histories = {}

def get_chat_history(session_id):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

async def chat_with_rag(message: str, session_id: str):
    history = get_chat_history(session_id)
    groq_client = get_groq_client()
    
    # TIER 1: PDF
    chunk = get_relevant_chunk(message, session_id)
    if chunk:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": f"Context: {chunk}\n\nQ: {message}"}],
            max_tokens=500
        )
        answer = response.choices[0].message.content
        history.append({"role": "user", "content": message})
        history.append({"role": "ai", "content": answer})
        return {"answer": answer, "source": "pdf"}
    
    # TIER 2: WEB
    try:
        web = await search_serper(message)
        if web:
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": f"Search: {web}\n\nQ: {message}"}],
                max_tokens=500
            )
            answer = response.choices[0].message.content
            history.append({"role": "user", "content": message})
            history.append({"role": "ai", "content": answer})
            return {"answer": answer, "source": "web_search"}
    except:
        pass
    
    # TIER 3: LLM
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": message}],
        max_tokens=500
    )
    answer = response.choices[0].message.content
    history.append({"role": "user", "content": message})
    history.append({"role": "ai", "content": answer})
    return {"answer": answer, "source": "llm"}
