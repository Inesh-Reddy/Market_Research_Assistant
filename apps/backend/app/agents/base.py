import time

from app.schemas.events import ExecutionEvent


async def emit(pub, ctx, event_type, agent, payload=None, started=None):
    ev = ExecutionEvent(execution_id=ctx.execution_id, conversation_id=ctx.conversation_id, event_type=event_type, agent_name=agent, payload=payload or {}, duration_ms=((time.time()-started)*1000 if started else None))
    await pub.publish(ev); return ev
