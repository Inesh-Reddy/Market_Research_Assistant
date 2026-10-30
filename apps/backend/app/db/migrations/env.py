import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

config=context.config
if config.config_file_name: fileConfig(config.config_file_name)
url=os.environ.get("DATABASE_URL","sqlite+aiosqlite:///./fip.db")
# Alembic async env: tables are also created via init_db() for local dev; migrations own prod schema.
from app.db import models  # noqa
from app.db.base import Base

target_metadata=Base.metadata
def run_migrations_offline():
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction(): context.run_migrations()
async def run_async():
    cfg=config.get_section(config.config_ini_section,{}); cfg["sqlalchemy.url"]=url
    eng=async_engine_from_config(cfg, prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with eng.connect() as conn: await conn.run_sync(lambda c: (context.configure(connection=c, target_metadata=target_metadata), context.begin_transaction().__enter__(), context.run_migrations()))
    await eng.dispose()
if context.is_offline_mode(): run_migrations_offline()
else: asyncio.run(run_async())
