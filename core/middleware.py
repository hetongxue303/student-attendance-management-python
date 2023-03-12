import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from core import logger
from core.config import settings


def middleware_init(app: FastAPI):
    cors_middleware(app)  # 配置跨域中间件
    http_middleware(app)  # 配置http中间件
    logger.success('中间件加载完成')


def cors_middleware(app: FastAPI):
    if settings.APP_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_methods=['*'],
            allow_headers=['*'],
            allow_credentials=True
        )


def http_middleware(app: FastAPI):
    @app.middleware("http")
    async def http_middleware_init(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 2))
        logger.debug('方法:{}  地址:{}  耗时:{} ms', request.method, request.url, str(round(process_time, 2)))
        return response
