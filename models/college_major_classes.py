from sqlalchemy import Column, BigInteger, ForeignKey

from models import Base


class College_Major_Classes(Base):
    __table_args__ = ({"comment": "学院专业班级表"})
    cmc_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    college_id = Column(BigInteger, ForeignKey('college.college_id'), comment='学院ID')
    major_id = Column(BigInteger, ForeignKey('major.major_id'), comment='专业ID')
    classes_id = Column(BigInteger, ForeignKey('classes.classes_id'), comment='班级ID')
