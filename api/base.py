from fastapi import APIRouter, FastAPI

from api.v1 import test, college, major, classes, auth
from core import logger

router = APIRouter(prefix='/v1')

router.include_router(test.router, tags=['测试模块'])
router.include_router(auth.router, tags=['权限模块'])
router.include_router(college.router, tags=['学院模块'], prefix='/college')
router.include_router(major.router, tags=['专业模块'], prefix='/major')
router.include_router(classes.router, tags=['班级模块'], prefix='/classes')


def init_router(app: FastAPI):
    logger.success('路由配置完毕')
    app.include_router(router, prefix='')
