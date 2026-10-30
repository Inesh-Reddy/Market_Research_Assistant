# API Specification (base /api/v1, OpenAPI at /docs is authoritative)
- POST /chat {question, conversation_id?, model_override?} → 202 {execution_id, conversation_id, status}
- GET /executions/{id} → status/metadata; 404 if unknown
- GET /executions/{id}/events → text/event-stream (named events = event_type; keepalive comments; history replay then live)
- GET /executions/{id}/result → ConsolidatedResult; 404 until ready
- GET /agents → agent list; GET /health → backend + LLM health; GET /prompts, GET /prompts/{agent_name}
Validation via Pydantic (question 3..2000 chars → 422). CORS allowlist via CORS_ORIGINS.
