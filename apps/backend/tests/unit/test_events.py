import asyncio

from app.orchestration.event_publisher import EventPublisher
from app.schemas.events import ExecutionEvent


def test_event_dedup():
    async def go():
        p=EventPublisher(); ev=ExecutionEvent(execution_id="e1",event_type="agent.started")
        await p.publish(ev); await p.publish(ev)
        assert len(p.history("e1"))==1
    asyncio.run(go())
