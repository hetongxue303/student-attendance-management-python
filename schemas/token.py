from datetime import timedelta

from pydantic import BaseModel

from schemas.menu import VOMenu


class VOLogin(BaseModel):
    user_id: int = None
    avatar: str = 'http://ts1.cn.mm.bing.net/th/id/R-C.dcbb013ce7246b6522d52f2af7472aac?rik=Tpd%2ffh%2bL6oMXmw&riu=http%3a%2f%2fwww.obzhi.com%2fwp-content%2fuploads%2f2021%2f01%2f51.jpg&ehk=WzScALuq7av9hw%2fIr7KmxvoKAL5keWN9rdvK1vas1uU%3d&risl=&pid=ImgRaw&r=0'
    username: str = None
    real_name: str = None
    is_admin: bool = None
    gender: int = None
    roles: list[str] = None
    is_status: bool = None
    permission: list[str] = None
    menus: list[VOMenu] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Token(BaseModel):
    code: int
    message: str
    access_token: str
    expired_time: timedelta
    user: VOLogin

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
