#!/usr/bin/env bash
set -e
cd apps/backend && uv run pytest -q
cd ../frontend && npx tsc --noEmit
