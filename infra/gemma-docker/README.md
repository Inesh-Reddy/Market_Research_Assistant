# Gemma Docker Infra
Start: `./start.sh` (idempotent) or `docker compose up -d`. Logs: `docker compose logs -f ollama`. Stop: `docker compose down`.
Ollama is exposed on http://localhost:11434 for the host-run backend. If the backend is later containerized, replace localhost with the `ollama` service hostname because localhost inside a container refers to that container.
Apple Silicon: the official ollama image runs natively on arm64; no platform override needed.
