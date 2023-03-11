import typing
from datetime import timedelta

from aioredis import Redis
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import Security
from core.config import settings
from core.security import captcha_check, authenticate, generate_token
from database.mysql import get_db
from database.redis import get_redis
from schemas.result import Result
from schemas.token import Token, VOLogin
from utils.captcha import generate_captcha

router = APIRouter()
db: Session = next(get_db())


@router.post('/login', response_model=Token, summary='登录认证')
async def login(data: OAuth2PasswordRequestForm = Depends(), code: str = Form()):
    if await captcha_check(code=code):
        user = await authenticate(username=data.username, password=data.password)
        # await set_current_user_info(user.user_id)
        # await generate_scopes()
        redis: Redis = await get_redis()
        # menus: list[MenuDto] = jsonpickle.decode(await redis.get('current-menu-data'))
        # role_key: list[str] = jsonpickle.decode(await redis.get('current-role-keys'))
        # scopes: list[str] = jsonpickle.decode(await redis.get('current-scopes'))
        token: str = await generate_token({'id': user.user_id, 'sub': user.username, 'scopes': []})
        login_info: VOLogin = VOLogin(username=user.username, real_name=user.real_name, menus=[],
                                      is_status=user.is_status, gender=user.gender, is_admin=user.is_admin)
        await redis.setex(name=Security.TOKEN, value=token, time=timedelta(milliseconds=settings.JWT_EXPIRE))
        # await redis.set(name='current-user', value=jsonpickle.encode(login_info))
        return Token(code=200,
                     message='登陆成功',
                     access_token=token,
                     expired_time=settings.JWT_EXPIRE,
                     user=login_info)


@router.get('/logout', response_model=Result, summary='用户注销')
async def logout():
    redis: Redis = await get_redis()
    redis_key: list[str] = []
    for key in redis_key:
        await redis.delete(key)
    return Result(message='注销成功')


@router.get('/captcha-image', response_model=Result[typing.Any], summary='获取验证码')
async def get_code():
    return Result(message='获取验证码成功', content=await generate_captcha())
