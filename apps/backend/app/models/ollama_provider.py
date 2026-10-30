import httpx

from app.core.exceptions import ProviderUnavailableError
from app.models.llm_provider import LLMProvider, LLMResponse


class OllamaProvider(LLMProvider):
    name = "ollama"
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model_id = model
    async def generate(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        prompt = f"{system_prompt}\n\n{user_prompt}"
        try:
            async with httpx.AsyncClient(timeout=60.0) as c:
                r = await c.post(f"{self.base_url}/api/generate", json={"model": self.model_id, "prompt": prompt, "stream": False})
                if r.status_code == 404:
                    raise ProviderUnavailableError(f"Ollama model '{self.model_id}' not found. Run: ollama pull {self.model_id}")
                r.raise_for_status()
                text = r.json().get("response", "").strip()
        except httpx.ConnectError as e:
            raise ProviderUnavailableError(f"Ollama unavailable at {self.base_url}: {e}") from e
        return LLMResponse(text=text or "(empty model response)", provider=self.name, model=self.model_id, prompt=prompt)
    async def health(self) -> dict:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                r = await c.get(f"{self.base_url}/api/tags")
                models = [m.get("name") for m in r.json().get("models", [])] if r.status_code==200 else []
                return {"provider":"ollama","base_url":self.base_url,"model":self.model_id,"reachable":r.status_code==200,"models":models,"model_available": self.model_id in models}
        except Exception as e:
            return {"provider":"ollama","base_url":self.base_url,"model":self.model_id,"reachable":False,"error":str(e),"models":[],"model_available":False}
    def strands_model(self):
        """Return Strands OllamaModel when strands-agents is installed, else None."""
        try:
            from strands.models.ollama import OllamaModel  # type: ignore
            return OllamaModel(host=self.base_url, model_id=self.model_id)
        except Exception:
            return None
