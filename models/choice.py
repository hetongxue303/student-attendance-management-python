from sqlalchemy import Column, BigInteger, Enum, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from models import Base


class Choice(Base):
    __table_args__ = ({"comment": "选课表"})
    choice_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='选课ID')

    user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False, comment='用户ID(选择的课程的学生)')
    user = relationship('User', backref='user3')

    course_id = Column(BigInteger, ForeignKey('course.course_id'), nullable=False, comment='课程ID(选择的课程)')
    course = relationship('Course', backref='course3')

    score = Column(DECIMAL(4, 1), server_default='0', comment='课程成绩')

    choice_status = Column(Enum('1', '2', '3'), nullable=False, server_default='1',
                           comment='选课状态(1未处理 2已同意 3已拒绝)')
