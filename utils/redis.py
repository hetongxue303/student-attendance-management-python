import jsonpickle
from aioredis import Redis

from core import Security
from database.redis import get_redis
from schemas.token import VOLogin


async def get_userinfo() -> VOLogin:
    redis: Redis = await get_redis()
    return jsonpickle.decode(await redis.get('userinfo'))


async def get_token():
    redis: Redis = await get_redis()
    return jsonpickle.decode(await redis.get(Security.TOKEN))
