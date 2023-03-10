from sqlalchemy import Column, String, BigInteger, Enum, ForeignKey

from models import Base


class User(Base):
    __table_args__ = ({"comment": "用户表"})
    user_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    username = Column(String(200), nullable=False, comment='账户')
    password = Column(String(200), nullable=False, comment='密码')
    real_name = Column(String(200), nullable=False, comment='姓名')
    gender = Column(Enum('1', '2'), nullable=False, comment='性别')
    is_status = Column(Enum('0', '1'), nullable=False, server_default='0', comment='用户状态')
    description = Column(String(500), nullable=False, server_default='无', comment='用户描述')
    classes_id = Column(BigInteger, ForeignKey('classes.classes_id'), comment='班级ID')
