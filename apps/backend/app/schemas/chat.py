
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    conversation_id: str | None = None
    model_override: str | None = None
class ChatResponse(BaseModel):
    execution_id: str
    conversation_id: str
    status: str
