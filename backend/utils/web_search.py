import httpx
import os

async def search_serper(query: str):
    """Search using Serper API (free tier available)"""
    api_key = os.getenv("SERPER_API_KEY")
    
    if not api_key:
        return None
    
    url = "https://google.serper.dev/search"
    payload = {"q": query}
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            data = response.json()
            
            # Extract top 3 results
            results = data.get("organic", [])[:3]
            context = "\n\n".join([f"{r['title']}\n{r['snippet']}" for r in results])
            return context
        except Exception as e:
            print(f"Serper search error: {e}")
            return None
