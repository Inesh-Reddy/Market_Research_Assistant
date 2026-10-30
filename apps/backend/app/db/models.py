import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def _uuid(): return str(uuid.uuid4())
def _now(): return datetime.now(UTC)
JSONType = JSON().with_variant(JSONB, "postgresql")

class Conversation(Base):
    __tablename__="conversations"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=_uuid)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

class Execution(Base):
    __tablename__="executions"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=_uuid)
    conversation_id: Mapped[str]=mapped_column(ForeignKey("conversations.id"), index=True)
    question: Mapped[str]=mapped_column(Text, default="")
    ticker: Mapped[str]=mapped_column(String(16), nullable=True)
    status: Mapped[str]=mapped_column(String(32), default="running", index=True)
    final_response: Mapped[str]=mapped_column(Text, default="")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

class AgentExecution(Base):
    __tablename__="agent_executions"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=_uuid)
    execution_id: Mapped[str]=mapped_column(ForeignKey("executions.id"), index=True)
    agent_name: Mapped[str]=mapped_column(String(64), index=True)
    status: Mapped[str]=mapped_column(String(32), default="pending")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=_now)

class ExecutionEventRow(Base):
    __tablename__="execution_events"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=_uuid)
    execution_id: Mapped[str]=mapped_column(String(36), index=True)
    conversation_id: Mapped[str]=mapped_column(String(36), default="")
    event_type: Mapped[str]=mapped_column(String(64), index=True)
    agent_name: Mapped[str]=mapped_column(String(64), nullable=True)
    payload: Mapped[dict]=mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=_now)

class AgentResultRow(Base):
    __tablename__="agent_results"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=_uuid)
    execution_id: Mapped[str]=mapped_column(ForeignKey("executions.id"), index=True)
    agent_name: Mapped[str]=mapped_column(String(64))
    result_json: Mapped[dict]=mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=_now)

class PromptVersion(Base):
    __tablename__="prompt_versions"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=_uuid)
    agent_name: Mapped[str]=mapped_column(String(64), index=True)
    version: Mapped[str]=mapped_column(String(32))
    content: Mapped[str]=mapped_column(Text, default="")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=_now)
