import aioredis
from aioredis import Redis
from fastapi import FastAPI

from core.config import settings


async def get_async_redis_pool() -> Redis:
    return Redis(connection_pool=aioredis.ConnectionPool.from_url(
        url=settings.REDIS_URL,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        encoding="utf-8",
        decode_responses=True
    ))


async def init_redis_pool(app: FastAPI):
    app.state.redis = await get_async_redis_pool()


async def get_redis() -> Redis:
    return await get_async_redis_pool()
