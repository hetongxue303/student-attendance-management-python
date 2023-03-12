import typing
from datetime import timedelta

import jsonpickle
from aioredis import Redis
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import Security
from core.config import settings
from core.security import captcha_check, authenticate, generate_token, get_current_user_menu, generate_scopes, \
    get_user_role
from database.mysql import get_db
from database.redis import get_redis
from models import User
from schemas.result import Result
from schemas.token import Token, VOLogin
from utils.captcha import generate_captcha

router = APIRouter()
db: Session = next(get_db())


@router.post('/login', response_model=Token, summary='登录认证')
async def login(data: OAuth2PasswordRequestForm = Depends(), code: str = Form()):
    if await captcha_check(code=code):
        redis: Redis = await get_redis()
        user: User = await authenticate(username=data.username, password=data.password)
        permission: list[str] = await generate_scopes(user_id=user.user_id)
        token: str = await generate_token({'id': user.user_id, 'sub': user.username, 'scopes': permission})
        userinfo: VOLogin = VOLogin(username=user.username, real_name=user.real_name, permission=permission,
                                    gender=user.gender, is_status=user.is_status, is_admin=user.is_admin,
                                    roles=await get_user_role(user_id=user.user_id),
                                    menus=await get_current_user_menu(user_id=user.user_id))
        await redis.setex(name=Security.TOKEN, value=token, time=timedelta(milliseconds=settings.JWT_EXPIRE))
        await redis.set(name='userinfo', value=jsonpickle.encode(userinfo))
        return Token(code=200, message='登陆成功', access_token=token, expired_time=settings.JWT_EXPIRE, user=userinfo)


@router.get('/logout', response_model=Result, summary='用户注销')
async def logout():
    redis: Redis = await get_redis()
    redis_key: list[str] = ['userinfo']
    for key in redis_key:
        await redis.delete(key)
    return Result(message='注销成功')


@router.get('/captcha-image', response_model=Result[typing.Any], summary='获取验证码')
async def get_code():
    return Result(message='获取验证码成功', content=await generate_captcha())
