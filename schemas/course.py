from datetime import datetime

from pydantic import BaseModel

from schemas.classes import VOClasses
from schemas.college import VOCollege
from schemas.major import VOMajor


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
