from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

_engine=None; _factory=None
def get_engine():
    global _engine,_factory
    if _engine is None:
        s=get_settings()
        _engine=create_async_engine(s.database_url, echo=False)
        _factory=async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)
    return _engine
def get_session_factory():
    get_engine(); return _factory
async def init_db():
    from app.db import models  # noqa
    from app.db.base import Base
    eng=get_engine()
    async with eng.begin() as conn: await conn.run_sync(Base.metadata.create_all)
