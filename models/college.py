from sqlalchemy import Column, BigInteger, String

from models import Base


class College(Base):
    __table_args__ = ({"comment": "学院表"})
    college_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='学院ID')
    college_name = Column(String(100), nullable=False, comment='学院名称')
    description = Column(String(500), server_default='空', comment='学院描述')
