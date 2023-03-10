import typing
from datetime import timedelta

from pydantic import BaseModel


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
