# ADR: SSE for execution streaming

Events are server→client only; SSE gives auto-reconnect, plain HTTP, and simple FastAPI StreamingResponse. WebSockets would add bidirectional complexity with no requirement.

Status: Accepted.
