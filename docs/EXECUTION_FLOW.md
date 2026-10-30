# Execution Flow
1. POST /chat creates ExecutionContext, returns 202 immediately; execution runs in background.
2. Coordinator emits execution.started, coordinator.started, model metadata, one coordinator.task_created per agent (with prompt_version).
3. orchestration.parallel_execution_started; three agents run concurrently (asyncio.gather), each emitting agent/tool started/completed/failed events.
4. result.validation_* (contradiction detection), coordinator.synthesis_started, optional model.request_* for Ollama synthesis, execution.completed.
5. Frontend subscribes with EventSource, replays history then streams live; GET /result returns the consolidated answer. Duplicate event_ids are dropped by the publisher.
