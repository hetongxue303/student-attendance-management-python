from sqlalchemy import Column, BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from models import Base


class Course(Base):
    __table_args__ = ({"comment": "课程表"})
    course_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='课程ID')

    course_name = Column(String(100), nullable=False, comment='课程名称')

    college_id = Column(BigInteger, ForeignKey('college.college_id'), nullable=False, comment='学院ID')
    college = relationship('College', backref='college1')

    major_id = Column(BigInteger, ForeignKey('major.major_id'), nullable=False, comment='专业ID')
    major = relationship('Major', backref='major1')

    classes_id = Column(BigInteger, ForeignKey('classes.classes_id'), nullable=False, comment='班级ID')
    classes = relationship('Classes', backref='classes1')

    count = Column(Integer, nullable=False, comment='课程人数')

    selection = Column(Integer, server_default='0', comment='已选人数')

    time = Column(Integer, nullable=False, comment='课程课时')

    description = Column(String(500), server_default='空', comment='课程描述')
