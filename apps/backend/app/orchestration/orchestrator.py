import asyncio

from app.agents.agent_factory import get_runner
from app.agents.coordinator import build_final_response, extract_ticker, sanitize_llm_output
from app.agents.prompt_loader import load_prompt
from app.orchestration.execution_context import ExecutionContext
from app.orchestration.result_aggregator import aggregate_sources, detect_contradictions
from app.schemas.events import ExecutionEvent
from app.schemas.execution import ConsolidatedResult


async def _emit(pub, ctx, et, agent, payload=None):
    await pub.publish(ExecutionEvent(execution_id=ctx.execution_id, conversation_id=ctx.conversation_id, event_type=et, agent_name=agent, payload=payload or {}))

async def run_execution(ctx: ExecutionContext, settings, publisher, llm_provider, store) -> ConsolidatedResult:
    """Coordinator: decompose -> parallel delegation -> validate -> synthesize. Bounded timeouts, partial-result tolerant."""
    await _emit(publisher, ctx, "execution.started", "coordinator", {"question": ctx.query})
    await _emit(publisher, ctx, "coordinator.started", "coordinator", {"provider": llm_provider.name, "model": llm_provider.model_id})
    ticker, company = extract_ticker(ctx.query)
    ctx.ticker, ctx.company = ticker, company
    await _emit(publisher, ctx, "model.request_completed", "coordinator", {"provider": llm_provider.name, "model": llm_provider.model_id, "note": "Gemma 3:270m tool-calling is unreliable; orchestration is deterministic, LLM used only for synthesis when available."})
    tasks = ["news_agent","financial_agent","sentiment_agent"]
    ctx.tasks = tasks
    for t in tasks:
        prompt = load_prompt(f"{t}.md")
        payload={"task":t,"ticker":ticker,"prompt_version":prompt["version"]}
        if settings.log_prompts: payload["system_prompt"]=prompt["content"]
        await _emit(publisher, ctx, "coordinator.task_created", "coordinator", payload)
    await _emit(publisher, ctx, "orchestration.parallel_execution_started", "coordinator", {"agents":tasks})
    async def _run(name):
        runner=get_runner(name)
        for attempt in range(settings.max_retries+1):
            try:
                return await asyncio.wait_for(runner(ctx, settings, publisher), timeout=settings.agent_timeout_s)
            except TimeoutError:
                if attempt < settings.max_retries:
                    await _emit(publisher, ctx, "agent.failed", name, {"error":"timeout","retry":attempt+1})
                    continue
                from app.schemas.agent import AgentResult
                return AgentResult(agent_name=name, execution_id=ctx.execution_id, status="failed", summary=f"{name} timed out", error="timeout")
    results = await asyncio.gather(*[_run(t) for t in tasks], return_exceptions=False)
    ctx.results=list(results)
    await _emit(publisher, ctx, "orchestration.parallel_execution_completed", "coordinator", {"completed":len(results)})
    await _emit(publisher, ctx, "result.validation_started", "coordinator", {})
    contradictions = detect_contradictions(ctx.results)
    await _emit(publisher, ctx, "result.validation_completed", "coordinator", {"contradictions":contradictions})
    await _emit(publisher, ctx, "coordinator.synthesis_started", "coordinator", {})
    # Deterministic full report first (complete data, clean formatting). LLM may add an overview only.
    final = build_final_response(ctx, ctx.results, contradictions)
    try:
        await _emit(publisher, ctx, "model.request_started", "coordinator", {"provider":llm_provider.name,"model":llm_provider.model_id})
        facts = "; ".join(f"{r.agent_name}={r.status}: {r.summary}" for r in ctx.results)[:1200]
        resp = await asyncio.wait_for(llm_provider.generate(
            "Write a 3-5 sentence factual overview. No headings, no lists, no instructions, cite nothing new.",
            f"Question: {ctx.query}. Ticker: {ticker}. Agent summaries: {facts}"), timeout=45.0)
        overview = sanitize_llm_output(resp.text)
        payload={"provider":resp.provider,"model":resp.model,"llm_overview_used": bool(overview)}
        if settings.log_prompts: payload["prompt"]=resp.prompt[:4000]
        await _emit(publisher, ctx, "model.request_completed", "coordinator", payload)
        if overview:
            final = build_final_response(ctx, ctx.results, contradictions, llm_overview=overview)
    except Exception as e:
        await _emit(publisher, ctx, "model.error", "coordinator", {"error":str(e),"fallback":"deterministic report retained"})
    ctx.final_response=final
    consolidated = ConsolidatedResult(execution_id=ctx.execution_id, conversation_id=ctx.conversation_id, question=ctx.query, ticker=ticker, final_response=final, agent_results=ctx.results, contradictions=contradictions, sources=aggregate_sources(ctx.results))
    store[ctx.execution_id]=consolidated
    await _emit(publisher, ctx, "execution.completed", "coordinator", {"status":"completed"})
    return consolidated
