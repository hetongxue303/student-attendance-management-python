from sqlalchemy import BigInteger, Column, ForeignKey

from models import Base


class User_Role(Base):
    __table_args__ = ({"comment": "用户角色表"})
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    user_id = Column(BigInteger, ForeignKey('user.user_id'), comment='用户ID')
    role_id = Column(BigInteger, ForeignKey('role.role_id'), comment='角色ID')
