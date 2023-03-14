from sqlalchemy import Column, BigInteger, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Check(Base):
    __table_args__ = ({"comment": "签到记录表"})
    check_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='签到ID')

    user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False, comment='签到用户ID')
    user = relationship('User', backref='user2')

    course_id = Column(BigInteger, ForeignKey('course.course_id'), nullable=False, comment='课程ID')
    course = relationship('Course', backref='course2')

    attendance_id = Column(BigInteger, ForeignKey('attendance.attendance_id'), nullable=False, comment='考勤ID')
    attendance = relationship('Attendance', backref='attendance1')

    check_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), comment='签到时间')
