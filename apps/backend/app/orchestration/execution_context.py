from dataclasses import dataclass, field

from app.schemas.agent import AgentResult


@dataclass
class ExecutionContext:
    execution_id: str
    conversation_id: str
    query: str
    ticker: str | None = None
    company: str | None = None
    tasks: list[str] = field(default_factory=list)
    results: list[AgentResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    final_response: str = ""
