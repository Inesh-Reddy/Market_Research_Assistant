from fastapi.testclient import TestClient

from app.main import create_app

client=TestClient(create_app())
def test_health(): assert client.get("/api/v1/health").status_code==200
def test_agents_and_prompts():
    assert client.get("/api/v1/agents").status_code==200
    assert client.get("/api/v1/prompts").status_code==200
    assert client.get("/api/v1/prompts/coordinator").status_code==200
def test_chat_validation(): assert client.post("/api/v1/chat", json={"question":"hi"}).status_code==422
def test_execution_404(): assert client.get("/api/v1/executions/nope").status_code==404
