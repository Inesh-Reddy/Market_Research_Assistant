import re
from datetime import UTC, datetime

from app.core.constants import TICKER_MAP
from app.tools.text_clean import clean_text

_PROMPT_MARKERS = ("# task", "# system", "# output", "# constraints", "plain markdown. every factual claim",
                   "given the user question and the three agent results", "you are the coordinator",
                   "prompt_version", "system prompt", "never fabricate financial")

def extract_ticker(query: str) -> tuple[str | None, str | None]:
    q = query.lower()
    for name, sym in TICKER_MAP.items():
        if name in q:
            return sym, name.title()
    m = re.search(r"\b([A-Z]{1,5})\b", query)
    if m and m.group(1) not in ("I", "A", "THE", "AND", "FOR", "STOCK"):
        return m.group(1), None
    return None, None

def sanitize_llm_output(text: str) -> str | None:
    """Accept LLM text only as a short overview. Reject prompt echo / instruction leakage."""
    if not text:
        return None
    low = text.lower()
    if any(m in low for m in _PROMPT_MARKERS):
        return None
    t = clean_text(text, max_chars=900)
    # Drop any leading echoed question/draft scaffolding.
    for sep in ("Overview:", "## Overview"):
        if sep in t:
            t = t.split(sep, 1)[1].strip()
            break
    if len(t) < 60 or "http" in t[:40]:
        return None
    return t

def _by_agent(results, name):
    return next((r for r in results if r.agent_name == name), None)

def build_final_response(ctx, results, contradictions, llm_overview: str | None = None) -> str:
    """Deterministic, complete report. Includes every finding/financial/source — no truncation."""
    title = f"{ctx.company or ''} ({ctx.ticker})".strip() if ctx.ticker else (ctx.company or ctx.query)
    news, fin, sent = _by_agent(results, "news_agent"), _by_agent(results, "financial_agent"), _by_agent(results, "sentiment_agent")
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# {title} — Research Report", "", f"> {ctx.query}", f"> Generated {now} · Sources cited inline · Not investment advice", ""]
    lines += ["## Overview", ""]
    if llm_overview:
        lines += [llm_overview, ""]
    bullets = []
    if fin:
        for fv in fin.financials:
            bullets.append(f"**{fv.label}:** {fv.value} {fv.currency} ({fv.source}, market {fv.market_timestamp or 'n/a'})")
    if sent and sent.sentiment:
        bullets.append(f"**Sentiment:** {sent.sentiment} — {clean_text(sent.summary, 220)}")
    if news:
        bullets.append(f"**News coverage:** {len(news.findings)} item(s), status {news.status}.")
    lines += [f"- {b}" for b in bullets] or ["- No structured data was returned by the agents; see sections below."]
    lines.append("")
    # News — full data
    lines += ["## Latest News", ""]
    if news and news.findings:
        for i, f in enumerate(news.findings, 1):
            src = f.sources[0] if f.sources else None
            head = f"[{f.title}]({src.url})" if src and src.url else f.title
            date = f" · {src.published_at}" if src and src.published_at else ""
            lines.append(f"{i}. **{head}**{date}")
            detail = clean_text(f.detail, 420)
            if detail:
                lines.append(f"   {detail}")
        if news.error:
            lines.append(f"Note: {news.error}")
    else:
        lines.append("_No news data available._")
    lines.append("")
    # Financials — full data as table + findings
    lines += ["## Financial Performance", ""]
    if fin and fin.financials:
        lines += ["| Metric | Value | Source | Market date | Retrieved |", "|---|---|---|---|---|"]
        for fv in fin.financials:
            lines.append(f"| {fv.label} | {fv.value} {fv.currency} | {fv.source} | {fv.market_timestamp or 'n/a'} | {fv.retrieved_at} |")
        lines.append("")
    if fin and fin.findings:
        for f in fin.findings:
            lines.append(f"- **{f.title}:** {clean_text(f.detail, 420)}")
    if fin and fin.error:
        lines.append(f"- _Provider note: {fin.error}_")
    if not fin or (not fin.financials and not fin.findings):
        lines.append("_No financial data available._")
    lines.append("")
    # Sentiment — full data
    lines += ["## Market Sentiment", ""]
    if sent:
        lines.append(f"**Overall: {sent.sentiment or 'unknown'}** — {clean_text(sent.summary, 300)}")
        lines.append("")
        for i, f in enumerate(sent.findings, 1):
            src = f.sources[0] if f.sources else None
            head = f"[{f.title}]({src.url})" if src and src.url else f.title
            lines.append(f"{i}. **{head}**")
            detail = clean_text(f.detail, 420)
            if detail:
                lines.append(f"   {detail}")
        if sent.error:
            lines.append(f"Note: {sent.error}")
    else:
        lines.append("_No sentiment data available._")
    lines.append("")
    # Risks / contradictions
    lines += ["## Risks & Contradictions", ""]
    risks = list(contradictions or [])
    for r in results:
        if r.status != "completed":
            risks.append(f"{r.agent_name} finished with status '{r.status}'" + (f": {r.error}" if r.error else ""))
    lines += [f"- {r}" for r in risks] or ["- No contradictions detected across agent outputs. Data gaps, if any, are noted per section."]
    lines += ["- Sentiment is an opinion summary, not a price prediction. Verify figures against primary filings before acting.", ""]
    # Sources — every unique URL
    seen, sources = set(), []
    for r in results:
        for s in r.sources:
            if s.url and s.url not in seen:
                seen.add(s.url)
                sources.append(s)
    lines += ["## Sources", ""]
    if sources:
        for i, s in enumerate(sources, 1):
            lines.append(f"{i}. [{s.title or s.url}]({s.url})" + (f" — {s.published_at}" if s.published_at else "") + (f" ({s.source})" if s.source else ""))
    else:
        lines.append("_No external sources were returned._")
    lines += ["", "---", "_Research information only — not investment advice._"]
    return "\n".join(lines)

# Backwards-compatible alias
def synthesize_fallback(ctx, results, contradictions) -> str:
    return build_final_response(ctx, results, contradictions)
