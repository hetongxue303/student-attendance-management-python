from sqlalchemy import Column, BigInteger, ForeignKey

from models import Base


class Student_Classes(Base):
    __table_args__ = ({"comment": "学生班级表"})
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    user_id = Column(BigInteger, ForeignKey('user.user_id'), comment='用户ID')
    classes_id = Column(BigInteger, ForeignKey('classes.classes_id'), comment='班级ID')
