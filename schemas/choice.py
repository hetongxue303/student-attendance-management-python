import decimal
from datetime import datetime

from pydantic import BaseModel

from schemas.course import VOCourse
from schemas.user import BOUser


class VOChoice(BaseModel):
    choice_id: int = None
    user_id: int = None
    user: BOUser = None
    course_id: int = None
    course: VOCourse = None
    score: decimal.Decimal = None
    choice_status: int = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VOChoiceBatch(BaseModel):
    ids: list[int] = None
    choice_status: int = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
