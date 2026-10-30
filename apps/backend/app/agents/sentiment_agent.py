import time
from datetime import UTC, datetime

from app.agents.base import emit
from app.core.exceptions import ToolError
from app.schemas.agent import AgentResult, Finding, SourceRef
from app.tools.tavily_tool import parse_tavily_response, tavily_search
from app.tools.text_clean import clean_text

POS=("bullish","upgrade","beat","growth","surge","rally","outperform","positive")
NEG=("bearish","downgrade","miss","decline","fall","risk","selloff","negative","lawsuit")

async def run_sentiment_agent(ctx, settings, publisher) -> AgentResult:
    t0=time.time(); started=datetime.now(UTC)
    await emit(publisher, ctx, "agent.started", "sentiment_agent", {"task":"sentiment analysis"})
    result = AgentResult(agent_name="sentiment_agent", execution_id=ctx.execution_id, started_at=started)
    query = f"{ctx.company or ctx.ticker or ctx.query} stock analyst sentiment outlook"
    try:
        await emit(publisher, ctx, "tool.started", "sentiment_agent", {"tool":"tavily_search","input":{"query":query}})
        data = await tavily_search(query, settings.tavily_api_key)
        items = parse_tavily_response(data)
        await emit(publisher, ctx, "tool.completed", "sentiment_agent", {"tool":"tavily_search","results":len(items)}, started=t0)
        pos=neg=0
        for it in items[:5]:
            text=(it["title"]+" "+(it["content"] or "")).lower()
            pos += sum(text.count(w) for w in POS); neg += sum(text.count(w) for w in NEG)
            src=SourceRef(title=it["title"], url=it["url"], published_at=it.get("published_date"), source="tavily")
            result.sources.append(src)
            result.findings.append(Finding(title=it["title"] or "Sentiment item", detail=clean_text(it["content"] or "", 420), sources=[src]))
        label = "mixed" if pos and neg and abs(pos-neg)<=2 else ("bullish" if pos>neg else ("bearish" if neg>pos else "neutral"))
        result.sentiment=label
        result.summary=f"Overall sentiment: {label} (positive signals {pos}, negative signals {neg}). This is an opinion summary, not a prediction."
        result.confidence=0.7 if items else 0.3
    except ToolError as e:
        result.status="partial"; result.error=str(e); result.sentiment="unknown"; result.summary="Sentiment search unavailable."
        result.findings.append(Finding(title="Sentiment unavailable", detail=str(e)))
        await emit(publisher, ctx, "tool.failed", "sentiment_agent", {"tool":"tavily_search","error":str(e)}, started=t0)
    except Exception as e:
        result.status="failed"; result.error=str(e); result.sentiment="unknown"; result.summary="Sentiment agent failed."
        await emit(publisher, ctx, "agent.failed", "sentiment_agent", {"error":str(e)}, started=t0)
    result.completed_at=datetime.now(UTC)
    await emit(publisher, ctx, "agent.completed", "sentiment_agent", {"status":result.status,"sentiment":result.sentiment}, started=t0)
    return result
