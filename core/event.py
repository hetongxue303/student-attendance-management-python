from fastapi import FastAPI

from api.base import init_router
from core import logger
from database.mysql import init_db
from database.redis import init_redis_pool
from exception.globals import init_exception


def app_init(app: FastAPI):
    @app.on_event('startup')
    async def startup():
        init_exception(app)  # 开启全局异常捕获
        init_db()  # 初始化数据库
        init_router(app)  # 注册路由
        await init_redis_pool(app)  # 初始化redis
        logger.success('启动成功')
        logger.success('访问文档: http://127.0.0.1:8000/docs')

    @app.on_event('shutdown')
    async def shutdown():
        await app.state.redis.close()
        logger.success('redis已关闭')
