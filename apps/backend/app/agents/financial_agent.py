import time
from datetime import UTC, datetime

from app.agents.base import emit
from app.schemas.agent import AgentResult, FinancialValue, Finding
from app.tools.alpha_vantage_tool import alpha_vantage_quote, parse_alpha_quote
from app.tools.yfinance_tool import parse_yfinance_history, yfinance_history


async def run_financial_agent(ctx, settings, publisher) -> AgentResult:
    t0=time.time(); started=datetime.now(UTC)
    await emit(publisher, ctx, "agent.started", "financial_agent", {"task":"financial analysis"})
    result = AgentResult(agent_name="financial_agent", execution_id=ctx.execution_id, started_at=started)
    symbol = ctx.ticker or "AAPL"
    retrieved = datetime.now(UTC).isoformat()
    errors=[]
    # Alpha Vantage
    try:
        await emit(publisher, ctx, "tool.started", "financial_agent", {"tool":"alpha_vantage_quote","input":{"symbol":symbol}})
        data = await alpha_vantage_quote(symbol, settings.alpha_vantage_api_key, timeout=settings.tool_timeout_s)
        q = parse_alpha_quote(data)
        await emit(publisher, ctx, "tool.completed", "financial_agent", {"tool":"alpha_vantage_quote","parsed":bool(q)}, started=t0)
        if q and q.get("price"):
            result.financials.append(FinancialValue(label="Latest price (Alpha Vantage)", value=q["price"], source="alpha_vantage", market_timestamp=q.get("latest_trading_day"), retrieved_at=retrieved))
            result.findings.append(Finding(title=f"{symbol} quote", detail=f"Price {q['price']} (change {q.get('change_percent')}), trading day {q.get('latest_trading_day')}. Live vs close depends on market hours."))
    except Exception as e:
        errors.append(f"Alpha Vantage: {e}")
        await emit(publisher, ctx, "tool.failed", "financial_agent", {"tool":"alpha_vantage_quote","error":str(e)}, started=t0)
    # yfinance fallback / complement
    try:
        await emit(publisher, ctx, "tool.started", "financial_agent", {"tool":"yfinance_history","input":{"symbol":symbol,"period":"1mo"}})
        data = await yfinance_history(symbol)
        parsed = parse_yfinance_history(data)
        await emit(publisher, ctx, "tool.completed", "financial_agent", {"tool":"yfinance_history","parsed":parsed}, started=t0)
        if parsed.get("latest_close"):
            result.financials.append(FinancialValue(label="Latest close (yfinance, historical)", value=parsed["latest_close"], source="yfinance", market_timestamp=parsed.get("latest_date"), retrieved_at=retrieved))
            result.findings.append(Finding(title=f"{symbol} 1-month history", detail=f"{parsed['points']} sessions, 1-month change {parsed['change_percent_1mo']}%, latest close {parsed['latest_close']} on {parsed.get('latest_date')} (historical close, not a live tick)."))
    except Exception as e:
        errors.append(f"yfinance: {e}")
        await emit(publisher, ctx, "tool.failed", "financial_agent", {"tool":"yfinance_history","error":str(e)}, started=t0)
    if result.financials:
        result.summary = f"Retrieved {len(result.financials)} financial value(s) for {symbol}."
        result.confidence = 0.85
    else:
        result.status = "partial" if errors else "failed"
        result.summary = "Financial data unavailable from both providers."
        result.error = "; ".join(errors)
        result.findings.append(Finding(title="Financial data unavailable", detail=result.error or "No data"))
        result.confidence = 0.2
    if errors and result.financials: result.error="; ".join(errors)
    result.completed_at=datetime.now(UTC)
    await emit(publisher, ctx, "agent.completed", "financial_agent", {"status":result.status,"values":len(result.financials)}, started=t0)
    return result
