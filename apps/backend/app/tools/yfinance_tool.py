import asyncio
from datetime import UTC, datetime


def _fetch_sync(symbol: str) -> dict:
    import yfinance as yf
    t = yf.Ticker(symbol)
    hist = t.history(period="1mo")
    rows=[]
    if hist is not None and not hist.empty:
        for idx, row in hist.tail(10).iterrows():
            rows.append({"date": str(idx.date()), "open": float(row["Open"]), "high": float(row["High"]), "low": float(row["Low"]), "close": float(row["Close"]), "volume": int(row["Volume"])})
    return {"symbol": symbol, "history": rows, "retrieved_at": datetime.now(UTC).isoformat()}

async def yfinance_history(symbol: str) -> dict:
    return await asyncio.to_thread(_fetch_sync, symbol)

def parse_yfinance_history(data: dict) -> dict:
    hist=data.get("history",[])
    if len(hist)>=2:
        first, last = hist[0]["close"], hist[-1]["close"]
        pct = ((last-first)/first*100) if first else 0.0
    else: pct=0.0
    return {"points": len(hist), "change_percent_1mo": round(pct,2), "latest_close": hist[-1]["close"] if hist else None, "latest_date": hist[-1]["date"] if hist else None}
