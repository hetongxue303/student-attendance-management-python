from sqlalchemy import Column, BigInteger, String

from models import Base


class Major(Base):
    __table_args__ = ({"comment": "专业表"})
    major_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='专业ID')
    major_name = Column(String(100), nullable=False, comment='专业名称')
    description = Column(String(500), server_default='空', comment='专业描述')
