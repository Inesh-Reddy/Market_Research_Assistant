from app.agents.coordinator import extract_ticker, synthesize_fallback
from app.agents.prompt_loader import list_prompts, load_prompt
from app.core.config import Settings
from app.models.factory import create_llm_provider
from app.orchestration.execution_context import ExecutionContext
from app.orchestration.result_aggregator import detect_contradictions
from app.schemas.agent import AgentResult
from app.tools.alpha_vantage_tool import parse_alpha_quote
from app.tools.tavily_tool import parse_tavily_response
from app.tools.yfinance_tool import parse_yfinance_history


def test_config_default_ollama_no_groq():
    s=Settings(llm_provider="ollama"); s.validate_provider()
    assert create_llm_provider(s).name=="ollama"

def test_config_bedrock_requires_model():
    import pytest
    with pytest.raises(ValueError): Settings(llm_provider="bedrock", bedrock_model_id="").validate_provider()

def test_prompt_loading():
    assert len(list_prompts())==4
    assert load_prompt("coordinator.md")["version"]=="v1"

def test_extract_ticker():
    assert extract_ticker("Analyze Apple stock")[0]=="AAPL"
    assert extract_ticker("latest on MSFT please")[0]=="MSFT"

def test_parse_alpha():
    assert parse_alpha_quote({"Global Quote":{"01. symbol":"AAPL","05. price":"200.5"}})["price"]==200.5
    assert parse_alpha_quote({}) is None

def test_parse_yfinance_and_tavily():
    assert parse_yfinance_history({"history":[{"date":"2024-01-01","close":100},{"date":"2024-01-02","close":110}]})["change_percent_1mo"]==10.0
    assert parse_tavily_response({"results":[{"title":"t","url":"u","content":"c"}]})[0]["title"]=="t"

def test_aggregator_partial():
    ctx=ExecutionContext(execution_id="e",conversation_id="c",query="Apple")
    r=AgentResult(agent_name="news_agent",execution_id="e",status="completed")
    assert isinstance(detect_contradictions([r]), list)
    assert "## Latest News" in synthesize_fallback(ctx,[r],[])
