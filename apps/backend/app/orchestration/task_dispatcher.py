# Dispatcher is implemented inside orchestrator via asyncio.gather (parallel, bounded retries/timeouts).
# Kept as a module boundary for future queue-based dispatch without changing callers.
