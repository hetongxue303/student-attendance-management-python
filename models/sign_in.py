from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, func, Integer, Enum
from sqlalchemy.orm import relationship

from models import Base


class Sign_In(Base):
    __table_args__ = ({"comment": "签到表"})
    sign_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='签到ID')

    attendance_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='考勤ID')
    attendance = relationship('Attendance', backref='attendance5')

    user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False, comment='用户ID')
    user = relationship('User', backref='user1')

    course_id = Column(BigInteger, ForeignKey('course.course_id'), nullable=False, comment='课程ID')
    course = relationship('Course', backref='course1')

    status = Column(Enum('0', '1'), nullable=False, server_default='0', comment='状态(1已结束 0签到中)')

    attendance_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), comment='发布考勤时间')
