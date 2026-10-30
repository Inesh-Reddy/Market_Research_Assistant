import uuid

from fastapi import APIRouter, BackgroundTasks, Request

from app.orchestration.execution_context import ExecutionContext
from app.orchestration.orchestrator import run_execution
from app.schemas.chat import ChatRequest, ChatResponse

router=APIRouter(tags=["chat"])
@router.post("/chat", response_model=ChatResponse, status_code=202)
async def chat(req: ChatRequest, request: Request, bg: BackgroundTasks):
    conv = req.conversation_id or str(uuid.uuid4())
    exid = str(uuid.uuid4())
    ctx = ExecutionContext(execution_id=exid, conversation_id=conv, query=req.question)
    request.app.state.contexts[exid]=ctx
    async def _run():
        try: await run_execution(ctx, request.app.state.settings, request.app.state.publisher, request.app.state.llm_provider, request.app.state.store)
        except Exception as e:
            from app.schemas.events import ExecutionEvent
            await request.app.state.publisher.publish(ExecutionEvent(execution_id=exid, conversation_id=conv, event_type="execution.completed", agent_name="coordinator", payload={"status":"failed","error":str(e)}))
    bg.add_task(_run)
    return ChatResponse(execution_id=exid, conversation_id=conv, status="running")
