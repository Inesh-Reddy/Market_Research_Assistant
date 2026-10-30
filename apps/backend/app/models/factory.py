from app.core.config import Settings
from app.models.bedrock_provider import BedrockProvider
from app.models.llm_provider import LLMProvider
from app.models.ollama_provider import OllamaProvider


def create_llm_provider(settings: Settings) -> LLMProvider:
    """Never falls back to Groq. Provider is explicit via LLM_PROVIDER."""
    p = settings.llm_provider.lower()
    if p == "ollama":
        return OllamaProvider(settings.ollama_base_url, settings.ollama_model)
    if p == "bedrock":
        return BedrockProvider(settings.bedrock_model_id, settings.aws_region)
    raise ValueError(f"Unsupported LLM_PROVIDER={settings.llm_provider}")
