from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from core.logger import logger
from exception.custom import *
from schemas.result import JSONResult


def init_exception(app: FastAPI):
    logger.success('全局异常捕获加载完成')

    @app.exception_handler(Exception)
    async def http_exception(request: Request, e: Exception):
        logger.error(e)
        return JSONResult(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器异常")

    @app.exception_handler(UnauthorizedException)
    async def http_exception(request: Request, e: UnauthorizedException):
        logger.error(e.message)
        return JSONResult(code=status.HTTP_401_UNAUTHORIZED, message=e.message)

    @app.exception_handler(SecurityScopeException)
    async def http_exception(request: Request, e: SecurityScopeException):
        logger.error(e.message)
        return JSONResult(code=e.code, message=e.message, headers=e.headers)

    @app.exception_handler(UserNotFoundException)
    async def http_exception(request: Request, e: UserNotFoundException):
        logger.error(e.message)
        return JSONResult(code=status.HTTP_400_BAD_REQUEST, message=e.message)

    @app.exception_handler(UserPasswordException)
    async def http_exception(request: Request, e: UserPasswordException):
        logger.error(e.message)
        return JSONResult(code=status.HTTP_400_BAD_REQUEST, message=e.message)

    @app.exception_handler(CaptchaException)
    async def http_exception(request: Request, e: CaptchaException):
        logger.error(e.message)
        return JSONResult(code=status.HTTP_400_BAD_REQUEST, message=e.message)

    @app.exception_handler(InsertException)
    async def http_exception(request: Request, e: InsertException):
        logger.error(e.message)
        return JSONResult(code=e.code, message=e.message)

    @app.exception_handler(DeleteException)
    async def http_exception(request: Request, e: DeleteException):
        logger.error(e.message)
        return JSONResult(code=e.code, message=e.message)

    @app.exception_handler(UpdateException)
    async def http_exception(request: Request, e: UpdateException):
        logger.error(e.message)
        return JSONResult(code=e.code, message=e.message)

    @app.exception_handler(QueryException)
    async def http_exception(request: Request, e: QueryException):
        logger.error(e.message)
        return JSONResult(code=e.code, message=e.message)
