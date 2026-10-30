from app.core.exceptions import ProviderUnavailableError
from app.models.llm_provider import LLMProvider, LLMResponse


class BedrockProvider(LLMProvider):
    name = "bedrock"
    def __init__(self, model_id: str, region: str = "us-east-1"):
        self.model_id = model_id; self.region = region
    async def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        # Future-ready: uses Strands BedrockModel when explicitly configured.
        try:
            from strands import Agent  # type: ignore
            from strands.models.bedrock import BedrockModel  # type: ignore
            model = BedrockModel(model_id=self.model_id, region_name=self.region)
            agent = Agent(model=model, system_prompt=system_prompt)
            result = agent(user_prompt)
            return LLMResponse(text=str(result), provider=self.name, model=self.model_id, prompt=user_prompt)
        except ImportError as e:
            raise ProviderUnavailableError("Bedrock selected but strands-agents not installed. Install: uv sync --extra strands") from e
    async def health(self) -> dict:
        return {"provider":"bedrock","model":self.model_id,"region":self.region,"reachable": bool(self.model_id),"note":"Bedrock health requires AWS credentials; verified at call time"}
