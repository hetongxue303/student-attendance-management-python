from datetime import datetime

from pydantic import BaseModel

from schemas.college import VOCollege
from schemas.major import VOMajor


class VOClasses(BaseModel):
    classes_id: int = None
    major_id: int = None
    major: VOMajor = None
    college_id: int = None
    college: VOCollege = None
    classes_name: str = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
