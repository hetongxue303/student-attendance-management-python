from datetime import datetime

from pydantic import BaseModel

from schemas.classes import VOClasses
from schemas.college import VOCollege
from schemas.major import VOMajor
from schemas.user import VOUser


class VOCourse(BaseModel):
    course_id: int = None
    course_name: str = None
    college_id: int = None
    college: VOCollege = None
    major_id: int = None
    major: VOMajor = None
    classes_id: int = None
    classes: VOClasses = None
    count: int = None
    time: int = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BOCourse(VOCourse):
    user_id: int = None
    user: VOUser = None


class VOMyCourse(VOCourse):
    checked_in: int = None  # 已签到次数
    not_checked_in: int = None  # 已签到次数
    remainder: int = None  # 剩余次数
