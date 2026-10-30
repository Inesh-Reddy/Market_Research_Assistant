from datetime import UTC, datetime

from pydantic import BaseModel, Field


def _now(): return datetime.now(UTC)

class SourceRef(BaseModel):
    title: str = ""
    url: str = ""
    published_at: str | None = None
    source: str = ""

class Finding(BaseModel):
    title: str
    detail: str
    sources: list[SourceRef] = Field(default_factory=list)

class FinancialValue(BaseModel):
    label: str
    value: float | None = None
    currency: str = "USD"
    source: str = ""
    market_timestamp: str | None = None
    retrieved_at: str = ""

class AgentResult(BaseModel):
    agent_name: str
    execution_id: str
    status: str = "completed"  # completed|failed|partial
    summary: str = ""
    findings: list[Finding] = Field(default_factory=list)
    sources: list[SourceRef] = Field(default_factory=list)
    financials: list[FinancialValue] = Field(default_factory=list)
    sentiment: str | None = None
    started_at: datetime = Field(default_factory=_now)
    completed_at: datetime | None = None
    error: str | None = None
    confidence: float = 0.5
