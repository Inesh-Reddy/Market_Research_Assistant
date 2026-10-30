# Multi-Agent Financial Intelligence Platform
Coordinator + News / Financial / Sentiment agents with full real-time observability (SSE), Ollama Gemma 3:270m local LLM, Tavily + Alpha Vantage + yfinance grounding, PostgreSQL history.
## Prerequisites
Python 3.12+ with uv, Node 20+, Docker. API keys: Tavily (https://tavily.com), Alpha Vantage (https://www.alphavantage.co) — yfinance and Ollama need no key. No Groq key is ever required with LLM_PROVIDER=ollama.
## Quick start (3 terminals)
```bash
# Terminal 1 — Ollama + Postgres
cd infra/gemma-docker && ./start.sh
# Terminal 2 — Backend  (API http://localhost:8000, Swagger http://localhost:8000/docs)
cd apps/backend && cp .env.example .env  # add TAVILY_API_KEY / ALPHA_VANTAGE_API_KEY
uv sync && uv run alembic upgrade head && uv run uvicorn app.main:app --reload --port 8000
# Terminal 3 — Frontend (http://localhost:5173)
cd apps/frontend && npm install && npm run dev
```
Or from root: `make infra-up`, `make backend`, `make frontend`, `make test`, `make check`.
Open http://localhost:5173, ask e.g. "Give me the latest analysis of Apple stock." Watch agents run in parallel and expand events in the terminal panel to inspect tool inputs/outputs and (with LOG_PROMPTS=true) prompts.
## Env vars
See `.env.example`. Key ones: LLM_PROVIDER (ollama default; bedrock optional, never silently Groq), OLLAMA_BASE_URL, OLLAMA_MODEL (any locally pulled model), DATABASE_URL, LOG_PROMPTS, TAVILY_API_KEY, ALPHA_VANTAGE_API_KEY.
## Docs
docs/HLD.md, docs/LLD.md, docs/AGENT_DESIGN.md, docs/PROMPT_ENGINEERING.md, docs/API_SPECIFICATION.md, docs/DATABASE_DESIGN.md, docs/EXECUTION_FLOW.md, docs/ADR/.
## Known limitations
Gemma 3:270m is small: synthesis quality is limited and tool-calling is unreliable, so orchestration is deterministic and the LLM only polishes synthesis (template fallback when Ollama is down). Without Tavily/Alpha keys those agents return explicit partial results instead of fabricating data.
