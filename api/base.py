from fastapi import APIRouter, FastAPI

from api.v1 import test
from core import logger

router = APIRouter(prefix='/v1')

router.include_router(test.router, tags=['测试模块'])


def init_router(app: FastAPI):
    logger.success('路由配置完毕')
    app.include_router(router, prefix='')
