from typing import Any

from pydantic import BaseModel, Field

from app.schemas.agent import AgentResult


class ExecutionStatus(BaseModel):
    execution_id: str
    conversation_id: str
    status: str
    question: str = ""
    ticker: str | None = None
    created_at: str = ""
class ConsolidatedResult(BaseModel):
    execution_id: str
    conversation_id: str
    question: str
    ticker: str | None = None
    final_response: str = ""
    agent_results: list[AgentResult] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    sources: list[dict[str, Any]] = Field(default_factory=list)
