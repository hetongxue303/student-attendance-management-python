from datetime import datetime

from pydantic import BaseModel

from schemas.course import VOCourse
from schemas.user import VOUser


class VOAttendance(BaseModel):
    attendance_id: int = None
    user_id: int = None
    user: VOUser = None
    course_id: int = None
    course: VOCourse = None
    attendance_time: datetime = None
    time: int = None
    status: int = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BOAttendance(VOAttendance):
    checked_count: int = None  # 签到人数
    is_checked: bool = None
