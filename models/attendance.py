from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, func, Integer
from sqlalchemy.orm import relationship

from models import Base


class Attendance(Base):
    __table_args__ = ({"comment": "考勤表"})
    attendance_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='考勤ID')

    user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False, comment='发布者ID')
    user = relationship('User', backref='user1')

    course_id = Column(BigInteger, ForeignKey('course.course_id'), nullable=False, comment='课程ID')
    course = relationship('Course', backref='course1')

    time = Column(Integer, nullable=False, comment='签到时长')

    attendance_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), comment='发布考勤时间')
