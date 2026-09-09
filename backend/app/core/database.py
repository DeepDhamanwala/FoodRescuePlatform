"""
Async SQLAlchemy engine and session factory.

Using asyncpg driver (DATABASE_URL must be postgresql+asyncpg://...).
Alembic uses the sync DATABASE_URL_SYNC for migrations only.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,          # set True in dev via env override if needed
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """All ORM models inherit from this base."""
    pass


async def get_db() -> AsyncSession:
    """FastAPI dependency: yields a DB session and guarantees close."""
    async with AsyncSessionLocal() as session:
        yield session
