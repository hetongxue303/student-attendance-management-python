from sqlalchemy import BigInteger, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Classes(Base):
    __table_args__ = ({"comment": "班级表"})
    classes_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='班级ID')
    classes_name = Column(String(100), nullable=False, comment='班级名称')
    description = Column(String(500), server_default='空', comment='班级描述')
    major_id = Column(BigInteger, ForeignKey('major.major_id'), comment='专业ID')
    major = relationship('Major', backref='major')
