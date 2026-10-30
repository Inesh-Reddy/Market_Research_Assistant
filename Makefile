infra-up:
	cd infra/gemma-docker && docker compose up -d
backend:
	cd apps/backend && uv run uvicorn app.main:app --reload --port 8000
frontend:
	cd apps/frontend && npm run dev
test:
	cd apps/backend && uv run pytest -q
lint:
	cd apps/backend && uv run ruff check app tests; cd apps/frontend && npx tsc --noEmit
check: lint test
