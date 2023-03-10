from datetime import datetime

from pydantic import BaseModel


class VOCollege(BaseModel):
    college_id: int = None
    college_name: str = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
