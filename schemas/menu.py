from datetime import datetime

from pydantic import BaseModel


class VOMenu(BaseModel):
    menu_id: int = None
    parent_id: int = None
    menu_title: str = None
    menu_type: int = None
    router_name: str = None
    router_path: str = None
    component: str = None
    sort: int = None
    icon: str = None
    permission: str = None
    sub_count: int = None
    is_show: bool = None
    is_sub: bool = None
    is_status: bool = None
    description: str = None
    create_time: datetime = None
    update_time: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VOMenuTree(VOMenu):
    children: list[VOMenu] = []
