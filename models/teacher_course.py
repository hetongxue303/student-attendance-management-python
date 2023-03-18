from sqlalchemy import Column, BigInteger, ForeignKey

from models import Base


class Teacher_Course(Base):
    __table_args__ = ({"comment": "教师课程表"})
    uc_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    user_id = Column(BigInteger, ForeignKey('user.user_id'), comment='用户ID')
    course_id = Column(BigInteger, ForeignKey('course.course_id'), comment='课程ID')
