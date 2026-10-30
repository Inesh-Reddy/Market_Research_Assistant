from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    prompt: str = ""

class LLMProvider(ABC):
    name: str = "base"
    model_id: str = ""
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse: ...
    @abstractmethod
    async def health(self) -> dict: ...
