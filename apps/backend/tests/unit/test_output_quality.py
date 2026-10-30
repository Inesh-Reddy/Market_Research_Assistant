from app.agents.coordinator import build_final_response, sanitize_llm_output
from app.orchestration.execution_context import ExecutionContext
from app.schemas.agent import AgentResult, FinancialValue, Finding, SourceRef
from app.tools.text_clean import clean_text


def _ctx(): return ExecutionContext(execution_id="e", conversation_id="c", query="Analyze Apple stock", ticker="AAPL", company="Apple")

def test_clean_text_strips_tables_and_footers():
    raw = "| Field | Value |\n| EPS | 1.9 | Apple Footer Shop and Learn Mac iPhone " + "word " * 200
    out = clean_text(raw)
    assert "Shop and Learn" not in out and "|" not in out and len(out) <= 430

def test_sanitize_rejects_prompt_echo():
    leaked = "Plain markdown. Every factual claim must trace. # Task Given the user question and the three agent results..."
    assert sanitize_llm_output(leaked) is None
    assert sanitize_llm_output("Apple shows steady iPhone demand with services growth supporting margins this quarter overall.") is not None

def test_full_data_no_truncation():
    findings=[Finding(title=f"Item {i}", detail="Detail "*10, sources=[SourceRef(title=f"Item {i}", url=f"https://x/{i}", source="tavily")]) for i in range(7)]
    news=AgentResult(agent_name="news_agent", execution_id="e", status="completed", summary="ok", findings=findings, sources=[f.sources[0] for f in findings])
    fin=AgentResult(agent_name="financial_agent", execution_id="e", status="completed", summary="ok",
                     financials=[FinancialValue(label="Price", value=348.91, source="alpha_vantage", market_timestamp="2026-10-29", retrieved_at="2026-10-30")])
    sent=AgentResult(agent_name="sentiment_agent", execution_id="e", status="completed", summary="mixed", sentiment="mixed")
    out=build_final_response(_ctx(), [news, fin, sent], [])
    for i in range(7): assert f"Item {i}" in out and f"https://x/{i}" in out
    assert "| Metric | Value |" in out and "348.91" in out
    assert "# Task" not in out and "Plain markdown" not in out
