from sqlalchemy import Column, BigInteger, String, Enum, Integer

from models import Base


class Menu(Base):
    __table_args__ = ({"comment": "菜单表"})
    menu_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='菜单ID')
    parent_id = Column(BigInteger, nullable=False, server_default='0', comment='父菜单ID')
    menu_title = Column(String(200), nullable=False, comment='菜单标题')
    menu_type = Column(Enum('1', '2', '3'), server_default='1', comment='菜单类型(1:菜单项 2:菜单 3:按钮)')
    router_name = Column(String(200), comment='路由名称')
    router_path = Column(String(200), comment='路由地址')
    component = Column(String(200), comment='组件地址')
    sort = Column(Integer, nullable=False, comment='菜单排序')
    icon = Column(String(200), comment='图标名称')
    permission = Column(String(200), comment='权限标识')
    sub_count = Column(Integer, nullable=False, server_default='0', comment='子菜单数')
    is_show = Column(Enum('0', '1'), nullable=False, server_default='1', comment='是否显示(1是 0否)')
    is_sub = Column(Enum('0', '1'), nullable=False, server_default='0', comment='是否有子菜单(1是 0否)')
    is_status = Column(Enum('0', '1'), nullable=False, server_default='1', comment='状态(1启用 0禁用)')
    description = Column(String(500), server_default='无', comment='菜单描述')
