from app.schemas.agent import AgentResult


def test_agent_result_schema():
    r=AgentResult(agent_name="news_agent",execution_id="e")
    d=r.model_dump(); assert d["agent_name"]=="news_agent" and "findings" in d
