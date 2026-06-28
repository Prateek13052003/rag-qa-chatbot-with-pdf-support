import os
from .rag import get_groq_client, get_vectorstore, get_embeddings_model
from .web_search import search_serper

chat_histories = {}

def get_chat_history(session_id):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

async def chat_with_rag(message: str, session_id: str):
    history = get_chat_history(session_id)
    groq_client = get_groq_client()
    
    # Tier 1: Try PDF
    try:
        embeddings_model = get_embeddings_model()
        query_embedding = embeddings_model.encode(message).tolist()
        collection = get_vectorstore(session_id)
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        
        if results.get("documents") and results["documents"][0]:
            context = "\n\n".join(results["documents"][0])
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": f"Context:\n{context}\n\nQ: {message}\n\nAnswer from context:"}],
                max_tokens=500,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            history.append({"role": "user", "content": message})
            history.append({"role": "ai", "content": answer})
            return {"answer": answer, "source": "pdf"}
    except:
        pass
    
    # Tier 2: Web Search
    try:
        web_context = await search_serper(message)
        if web_context:
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": f"Search results:\n{web_context}\n\nQ: {message}"}],
                max_tokens=500,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            history.append({"role": "user", "content": message})
            history.append({"role": "ai", "content": answer})
            return {"answer": answer, "source": "web_search"}
    except:
        pass
    
    # Tier 3: Direct LLM
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": message}],
        max_tokens=500,
        temperature=0.7
    )
    answer = response.choices[0].message.content
    history.append({"role": "user", "content": message})
    history.append({"role": "ai", "content": answer})
    return {"answer": answer, "source": "llm"}
