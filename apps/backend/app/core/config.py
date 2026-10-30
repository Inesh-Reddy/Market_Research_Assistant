from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "Financial Intelligence Platform"
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:270m"
    bedrock_model_id: str = ""
    aws_region: str = "us-east-1"
    groq_api_key: str = ""
    tavily_api_key: str = ""
    alpha_vantage_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///./fip.db"
    log_prompts: bool = False
    cors_origins: str = "http://localhost:5173"
    agent_timeout_s: float = 60.0
    tool_timeout_s: float = 20.0
    max_retries: int = 2

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def validate_provider(self) -> None:
        p = self.llm_provider.lower()
        if p not in ("ollama", "bedrock"):
            raise ValueError(f"Unsupported LLM_PROVIDER={self.llm_provider!r}; use 'ollama' or 'bedrock'")
        if p == "bedrock" and not self.bedrock_model_id:
            raise ValueError("LLM_PROVIDER=bedrock requires BEDROCK_MODEL_ID")

@lru_cache
def get_settings() -> Settings:
    s = Settings()
    s.validate_provider()
    return s
