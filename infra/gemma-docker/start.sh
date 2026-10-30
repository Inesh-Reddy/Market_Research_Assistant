#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
MODEL="${OLLAMA_MODEL:-gemma3:270m}"
echo "Starting Ollama + PostgreSQL..."
docker compose up -d
echo -n "Waiting for Ollama"
for i in $(seq 1 60); do
  if curl -sf http://localhost:11434/api/tags >/dev/null 2>&1; then echo " OK"; break; fi
  echo -n "."; sleep 2
  if [ "$i" = "60" ]; then echo; echo "ERROR: Ollama did not become healthy"; exit 1; fi
done
if curl -s http://localhost:11434/api/tags | grep -q "$MODEL"; then
  echo "Model $MODEL already available (skip pull)."
else
  echo "Pulling $MODEL (first run only)..."
  docker exec fip-ollama ollama pull "$MODEL"
fi
echo "Verifying model..."
curl -s http://localhost:11434/api/tags
echo
echo "Ollama endpoint: http://localhost:11434"
echo "PostgreSQL: localhost:5432 (db fip)"
echo "SUCCESS: Gemma infra ready."
