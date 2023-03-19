from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship

from models import Base


class Sign_In(Base):
    __table_args__ = ({"comment": "签到表"})
    sign_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='签到ID')

    attendance_id = Column(BigInteger, ForeignKey('attendance.attendance_id'), nullable=False, comment='考勤ID')
    attendance = relationship('Attendance', backref='attendance5')

    user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False, comment='用户ID')
    user = relationship('User', backref='user5')

    course_id = Column(BigInteger, ForeignKey('course.course_id'), nullable=False, comment='课程ID')
    course = relationship('Course', backref='course5')

    status = Column(Enum('0', '1', '2'), nullable=False, server_default='0', comment='状态(0待处理 1已签到 2缺勤)')

    sign_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), comment='签到时间')
