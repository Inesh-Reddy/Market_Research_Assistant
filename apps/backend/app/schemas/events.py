import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class ExecutionEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    execution_id: str
    conversation_id: str = ""
    event_type: str
    agent_name: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    duration_ms: float | None = None
    payload: dict[str, Any] = Field(default_factory=dict)

    def to_sse(self) -> str:
        return f"event: {self.event_type}\ndata: {self.model_dump_json()}\n\n"
