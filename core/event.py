from fastapi import FastAPI

from api.base import init_router
from core import logger
from core.middleware import middleware_init
from database.mysql import init_db
from database.redis import init_redis_pool
from exception.globals import init_exception


def app_init(app: FastAPI):
    @app.on_event('startup')
    async def startup():
        init_exception(app)
        init_db()
        middleware_init(app)
        await init_redis_pool(app)
        init_router(app)
        logger.success('项目启动成功')
        logger.success('API文档: http://127.0.0.1:8000/docs')

    @app.on_event('shutdown')
    async def shutdown():
        await app.state.redis.close()
        logger.success('redis已关闭')
