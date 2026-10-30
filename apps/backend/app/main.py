from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import agents, chat, executions, health
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.models.factory import create_llm_provider
from app.orchestration.event_publisher import EventPublisher


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    try:
        from app.db.session import init_db
        await init_db()
    except Exception:
        pass  # DB optional for local dev; in-memory store still works. Set DATABASE_URL for Postgres.
    yield

def create_app() -> FastAPI:
    settings=get_settings()
    app=FastAPI(title="Financial Intelligence Platform", version="0.1.0", lifespan=lifespan)
    app.state.settings=settings
    app.state.llm_provider=create_llm_provider(settings)
    app.state.publisher=EventPublisher()
    app.state.store={}
    app.state.contexts={}
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(chat.router, prefix="/api/v1")
    app.include_router(executions.router, prefix="/api/v1")
    app.include_router(agents.router, prefix="/api/v1")
    @app.get("/")
    async def root(): return {"service":"financial-intelligence-backend","docs":"/docs"}
    return app

app=create_app()
