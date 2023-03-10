from datetime import datetime

from pydantic import BaseModel


class BOUser(BaseModel):
    user_id: int = None
    username: str = None
    real_name: str = None
    gender: int = None
    is_status: bool = None
    is_admin: bool = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VOUser(BOUser):
    password: str = None
