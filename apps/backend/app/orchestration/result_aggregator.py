from app.schemas.agent import AgentResult


def detect_contradictions(results: list[AgentResult]) -> list[str]:
    out=[]
    sentiments=[r.sentiment for r in results if r.sentiment]
    news_ok = any(r.agent_name=="news_agent" and r.status=="completed" for r in results)
    fin_ok = any(r.agent_name=="financial_agent" and r.status=="completed" for r in results)
    if news_ok and not fin_ok:
        out.append("News data available but financial data missing — cross-check price claims against financial agent output.")
    # sentiment vs news tone mismatch heuristic
    s = " ".join(sentiments).lower()
    if "bullish" in s and any("decline" in (f.detail+f.title).lower() for r in results for f in r.findings):
        out.append("Sentiment is bullish while some findings mention declines — treat outlook as mixed.")
    return out

def aggregate_sources(results: list[AgentResult]) -> list[dict]:
    seen=set(); out=[]
    for r in results:
        for s in r.sources:
            if s.url and s.url not in seen:
                seen.add(s.url); out.append({"title": s.title, "url": s.url, "source": s.source, "published_at": s.published_at})
    return out
