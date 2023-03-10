from sqlalchemy import Column, BigInteger, String, Enum

from models import Base


class Role(Base):
    __table_args__ = ({"comment": "角色表"})
    role_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='角色ID')
    role_name = Column(String(50), nullable=False, comment='角色名称')
    role_code = Column(String(100), nullable=False, comment='角色代码')
    is_status = Column(Enum('0', '1'), nullable=False, server_default='0', comment='状态(1启用 0禁用)')
    description = Column(String(500), server_default='空', comment='角色描述')
