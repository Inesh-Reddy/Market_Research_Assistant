import httpx

from app.core.exceptions import ToolError


async def tavily_search(query: str, api_key: str, max_results: int = 5, timeout: float = 20.0) -> dict:
    """Real Tavily call. Raises ToolError with actionable message when unconfigured."""
    if not api_key:
        raise ToolError("TAVILY_API_KEY not configured. Get a key at https://tavily.com and set TAVILY_API_KEY in apps/backend/.env")
    async with httpx.AsyncClient(timeout=timeout) as c:
        r = await c.post("https://api.tavily.com/search", json={"api_key": api_key, "query": query, "max_results": max_results, "search_depth": "basic", "include_answer": False})
        if r.status_code == 429:
            raise ToolError("Tavily rate limit (429). Retry later or reduce request rate.")
        r.raise_for_status()
        return r.json()

def parse_tavily_response(data: dict) -> list[dict]:
    out=[]
    for item in data.get("results", []):
        out.append({"title": item.get("title",""), "url": item.get("url",""), "content": item.get("content",""), "published_date": item.get("published_date")})
    return out
