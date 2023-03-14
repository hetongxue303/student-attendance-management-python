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
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
