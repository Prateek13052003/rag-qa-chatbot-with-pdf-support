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
    
    # TIER 1: PDF
    try:
        embeddings_model = get_embeddings_model()
        query_embedding = embeddings_model.encode(message).tolist()
        collection = get_vectorstore(session_id)
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        
        if results["documents"][0]:
            context = "\n".join(results["documents"][0])
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": f"Context:\n{context}\n\nQ: {message}\nAnswer from context only:"}],
                max_tokens=500
            )
            answer = response.choices[0].message.content
            history.append({"role": "user", "content": message})
            history.append({"role": "ai", "content": answer})
            return {"answer": answer, "source": "pdf"}
    except:
        pass
    
    # TIER 2: WEB SEARCH
    try:
        web_results = await search_serper(message)
        if web_results:
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": f"Based on this search:\n{web_results}\n\nAnswer the question: {message}"}],
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
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": message}],
        max_tokens=500
    )
    answer = response.choices[0].message.content
    history.append({"role": "user", "content": message})
    history.append({"role": "ai", "content": answer})
    return {"answer": answer, "source": "llm"}
