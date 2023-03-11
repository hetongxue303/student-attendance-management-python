import typing
from datetime import timedelta

from pydantic import BaseModel

from schemas.menu import VOMenu


class Token(BaseModel):
    code: int
    message: str
    access_token: str
    expired_time: timedelta
    user: typing.Any

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VOLogin(BaseModel):
    username: str = None
    real_name: str = None
    is_admin: bool = None
    gender: str = None
    is_status: bool = None
    menus: list[VOMenu] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
