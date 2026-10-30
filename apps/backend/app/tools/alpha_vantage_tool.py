import httpx

from app.core.exceptions import ToolError


async def alpha_vantage_quote(symbol: str, api_key: str, timeout: float = 20.0) -> dict:
    if not api_key:
        raise ToolError("ALPHA_VANTAGE_API_KEY not configured. Get a free key at https://www.alphavantage.co and set ALPHA_VANTAGE_API_KEY in apps/backend/.env")
    async with httpx.AsyncClient(timeout=timeout) as c:
        r = await c.get("https://www.alphavantage.co/query", params={"function":"GLOBAL_QUOTE","symbol":symbol,"apikey":api_key})
        r.raise_for_status()
        data=r.json()
        if "Note" in data or "Information" in data:
            raise ToolError(f"Alpha Vantage rate limit: {data.get('Note') or data.get('Information')}")
        return data

def parse_alpha_quote(data: dict) -> dict | None:
    q = data.get("Global Quote") or {}
    if not q: return None
    try: price=float(q.get("05. price", 0)) or None
    except Exception: price=None
    return {"symbol": q.get("01. symbol"), "price": price, "change_percent": q.get("10. change percent"), "latest_trading_day": q.get("07. latest trading day"), "previous_close": q.get("08. previous close")}
