import asyncio
from collections import defaultdict

from app.schemas.events import ExecutionEvent


class EventPublisher:
    """In-memory fan-out for SSE + optional DB persistence hook. Idempotent by event_id."""
    def __init__(self):
        self._subs: dict[str, list[asyncio.Queue]] = defaultdict(list)
        self._history: dict[str, list[ExecutionEvent]] = defaultdict(list)
        self._seen: set[str] = set()
        self.on_event = None  # async callable(event) for persistence
    async def publish(self, event: ExecutionEvent) -> None:
        if event.event_id in self._seen: return
        self._seen.add(event.event_id)
        self._history[event.execution_id].append(event)
        for q in list(self._subs[event.execution_id]):
            await q.put(event)
        if self.on_event:
            try: await self.on_event(event)
            except Exception: pass
    def subscribe(self, execution_id: str) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self._subs[execution_id].append(q)
        return q
    def unsubscribe(self, execution_id: str, q) -> None:
        try: self._subs[execution_id].remove(q)
        except ValueError: pass
    def history(self, execution_id: str) -> list[ExecutionEvent]:
        return list(self._history.get(execution_id, []))
