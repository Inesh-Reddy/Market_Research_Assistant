#!/usr/bin/env bash
set -e
echo "1) Infra:  cd infra/gemma-docker && ./start.sh"
echo "2) Backend: cd apps/backend && uv sync && uv run uvicorn app.main:app --reload --port 8000"
echo "3) Frontend: cd apps/frontend && npm install && npm run dev"
echo "Open http://localhost:5173"
