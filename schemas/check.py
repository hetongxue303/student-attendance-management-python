from datetime import datetime

from pydantic import BaseModel

from schemas.attendance import VOAttendance
from schemas.course import VOCourse
from schemas.user import VOUser


class VOCheck(BaseModel):
    check_id: int = None
    user_id: int = None
    user: VOUser = None
    course_id: int = None
    course: VOCourse = None
    attendance_id: int = None
    attendance: VOAttendance = None
    status: int = None
    check_time: datetime = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
