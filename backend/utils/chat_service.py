import os
from .rag import get_groq_client, get_vectorstore, get_embeddings_model

chat_histories = {}

def get_chat_history(session_id):
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    return chat_histories[session_id]

async def chat_with_rag(message: str, session_id: str):
    history = get_chat_history(session_id)
    
    try:
        groq_client = get_groq_client()
        
        # Get vectorstore and search for relevant chunks
        try:
            embeddings_model = get_embeddings_model()
            query_embedding = embeddings_model.encode(message).tolist()
            collection = get_vectorstore(session_id)
            results = collection.query(query_embeddings=[query_embedding], n_results=3)
            
            if results.get("documents") and results["documents"][0]:
                context = "\n\n".join(results["documents"][0])
                prompt = f"Context from PDF:\n{context}\n\nQuestion: {message}\n\nAnswer based on the context:"
            else:
                prompt = message
        except:
            prompt = message
        
        # Call Groq LLM
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        answer = response.choices[0].message.content
        history.append({"role": "user", "content": message})
        history.append({"role": "ai", "content": answer})
        return {"answer": answer, "source": "pdf_rag"}
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "ai", "content": error_msg})
        return {"answer": error_msg, "source": "error"}
