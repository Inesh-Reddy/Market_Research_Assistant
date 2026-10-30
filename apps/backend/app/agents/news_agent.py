import time
from datetime import UTC, datetime

from app.agents.base import emit
from app.core.exceptions import ToolError
from app.schemas.agent import AgentResult, Finding, SourceRef
from app.tools.tavily_tool import parse_tavily_response, tavily_search
from app.tools.text_clean import clean_text


async def run_news_agent(ctx, settings, publisher) -> AgentResult:
    t0=time.time(); started=datetime.now(UTC)
    await emit(publisher, ctx, "agent.started", "news_agent", {"task":"news research"})
    result = AgentResult(agent_name="news_agent", execution_id=ctx.execution_id, started_at=started)
    query = f"{ctx.company or ctx.ticker or ctx.query} latest news earnings"
    try:
        await emit(publisher, ctx, "tool.started", "news_agent", {"tool":"tavily_search","input":{"query":query}})
        data = await tavily_search(query, settings.tavily_api_key)
        items = parse_tavily_response(data)
        await emit(publisher, ctx, "tool.completed", "news_agent", {"tool":"tavily_search","results":len(items)}, started=t0)
        for it in items[:5]:
            src=SourceRef(title=it["title"], url=it["url"], published_at=it.get("published_date"), source="tavily")
            result.sources.append(src)
            result.findings.append(Finding(title=it["title"] or "News item", detail=clean_text(it["content"] or "", 420), sources=[src]))
        result.summary = f"Found {len(result.findings)} recent news items for {ctx.ticker or ctx.company}." if result.findings else "No recent news items returned."
        result.confidence = 0.8 if result.findings else 0.3
    except ToolError as e:
        result.status="partial"; result.error=str(e); result.summary="News search unavailable."
        result.findings.append(Finding(title="News unavailable", detail=str(e)))
        await emit(publisher, ctx, "tool.failed", "news_agent", {"tool":"tavily_search","error":str(e)}, started=t0)
    except Exception as e:
        result.status="failed"; result.error=str(e); result.summary="News agent failed."
        await emit(publisher, ctx, "agent.failed", "news_agent", {"error":str(e)}, started=t0)
    result.completed_at=datetime.now(UTC)
    await emit(publisher, ctx, "agent.completed", "news_agent", {"status":result.status,"findings":len(result.findings)}, started=t0)
    return result
