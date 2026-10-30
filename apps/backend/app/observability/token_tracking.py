# Token tracking: Ollama responses do not always return token counts; record chars as proxy.
def approx_tokens(text: str) -> int: return max(1, len(text)//4)
