from datetime import datetime

from pydantic import BaseModel


class VORole(BaseModel):
    role_id: int = None
    role_name: str = None
    role_code: str = None
    is_status: bool = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BORole(BaseModel):
    role: VORole = None
    menu_ids: list[int] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
