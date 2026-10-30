# ADR: Use Strands-compatible providers with deterministic orchestration

Strands supplies model adapters (Ollama/Bedrock). Orchestration itself is deterministic asyncio because Gemma 3:270m tool-calling is unreliable; this keeps Strands benefits without depending on small-model tool use.

Status: Accepted.
