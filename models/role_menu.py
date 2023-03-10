from sqlalchemy import BigInteger, Column, ForeignKey

from models import Base


class Role_Menu(Base):
    __table_args__ = ({"comment": "角色菜单表"})
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    role_id = Column(BigInteger, ForeignKey('role.role_id'), comment='角色ID')
    menu_id = Column(BigInteger, ForeignKey('menu.menu_id'), comment='菜单ID')
