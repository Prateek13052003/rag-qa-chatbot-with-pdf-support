import os
from .rag import get_vectorstore, embeddings_model, get_groq_client
import httpx

chat_histories = {}

def get_chat_history(session_id):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

async def chat_with_rag(message: str, session_id: str):
    """RAG + LLM with 3-tier fallback"""
    history = get_chat_history(session_id)
    groq_client = get_groq_client()
    
    try:
        collection = get_vectorstore(session_id)
        query_embedding = embeddings_model.encode(message).tolist()
        print("BEFORE QUERY")
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        print("AFTER QUERY")
        print(results)
        print("RESULTS =", results)
        print("DOCUMENTS =", results.get("documents"))
        
        if results.get("documents") and results["documents"][0]:
            context = "\n\n".join(results["documents"][0])
            prompt = f"Context:\n{context}\n\nQuestion: {message}\n\nAnswer based ONLY on context:"
            
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            answer = response.choices[0].message.content    
            history.append({"role": "user", "content": message})
            history.append({"role": "ai", "content": answer})
            return {"answer": answer, "source": "pdf"}
    except Exception as e:
        print("RAG ERROR:", e)
        raise

    

    
    # Fallback: Direct LLM
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": message}],
        max_tokens=500
    )
    answer = response.choices[0].message.content
    history.append({"role": "user", "content": message})
    history.append({"role": "ai", "content": answer})
    return {"answer": answer, "source": "llm"}
