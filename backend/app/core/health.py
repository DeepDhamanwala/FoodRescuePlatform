"""
Health check endpoints for Docker Compose healthcheck / k8s probes.

Per Section I:
  - GET /health — liveness (process is up)
  - GET /ready — readiness (DB + Redis reachable)
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from redis import asyncio as aioredis

from app.core.database import engine
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """
    Liveness probe: returns 200 if the process is running.
    No external dependencies checked.
    """
    return {"status": "ok"}


@router.get("/ready")
async def readiness():
    """
    Readiness probe: returns 200 only if DB and Redis are reachable.
    Use this in Docker Compose healthcheck so dependent services wait.
    """
    checks = {}

    # Check database
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"

    # Check Redis
    try:
        redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        await redis.ping()
        await redis.close()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"

    # Fail if any check failed
    if any(v != "ok" for v in checks.values()):
        raise HTTPException(status_code=503, detail={"status": "not_ready", "checks": checks})

    return {"status": "ready", "checks": checks}
