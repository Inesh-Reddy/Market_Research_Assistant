import asyncio

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

router=APIRouter(tags=["executions"])
@router.get("/executions/{execution_id}")
async def get_execution(execution_id: str, request: Request):
    ctx=request.app.state.contexts.get(execution_id)
    result=request.app.state.store.get(execution_id)
    if not ctx and not result: raise HTTPException(404, "execution not found")
    return {"execution_id":execution_id,"conversation_id":(ctx.conversation_id if ctx else result.conversation_id),"status":("completed" if result else "running"),"question":(ctx.query if ctx else result.question),"ticker":(ctx.ticker if ctx else result.ticker),"events":len(request.app.state.publisher.history(execution_id))}
@router.get("/executions/{execution_id}/result")
async def get_result(execution_id: str, request: Request):
    result=request.app.state.store.get(execution_id)
    if not result: raise HTTPException(404, "result not ready")
    return result
@router.get("/executions/{execution_id}/events")
async def stream_events(execution_id: str, request: Request):
    pub=request.app.state.publisher
    # allow subscribing before execution starts; 404 only if never seen and no context
    async def gen():
        q=pub.subscribe(execution_id)
        try:
            for ev in pub.history(execution_id): yield ev.to_sse()
            while True:
                if await request.is_disconnected(): break
                try: ev=await asyncio.wait_for(q.get(), timeout=15.0)
                except TimeoutError: yield ": keepalive\n\n"; continue
                yield ev.to_sse()
                if ev.event_type=="execution.completed": break
        finally: pub.unsubscribe(execution_id, q)
    return StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
