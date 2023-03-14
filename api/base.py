from fastapi import APIRouter, FastAPI

from api.v1 import test, college, major, classes, security, user, role, menu, course, check
from core import logger

router = APIRouter(prefix='/v1')

router.include_router(test.router, tags=['测试模块'])
router.include_router(security.router, tags=['安全模块'])
router.include_router(user.router, tags=['用户模块'], prefix='/user')
router.include_router(role.router, tags=['角色模块'], prefix='/role')
router.include_router(menu.router, tags=['菜单模块'], prefix='/menu')
router.include_router(college.router, tags=['学院模块'], prefix='/college')
router.include_router(major.router, tags=['专业模块'], prefix='/major')
router.include_router(classes.router, tags=['班级模块'], prefix='/classes')
router.include_router(course.router, tags=['课程模块'], prefix='/course')
router.include_router(check.router, tags=['签到模块'], prefix='/check')


def init_router(app: FastAPI):
    logger.success('路由加载完成')
    app.include_router(router, prefix='')
