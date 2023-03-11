from pydantic import BaseModel


class BOUser(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
