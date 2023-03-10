import aioredis

from aioredis import Redis
from fastapi import FastAPI


async def get_async_redis_pool() -> Redis:
    return Redis(connection_pool=aioredis.ConnectionPool.from_url(
        url='redis://127.0.0.1',
        port=6379,
        db=1,
        encoding="utf-8",
        decode_responses=True
    ))


async def init_redis_pool(app: FastAPI):
    app.state.redis = await get_async_redis_pool()


async def get_redis() -> Redis:
    return await get_async_redis_pool()
