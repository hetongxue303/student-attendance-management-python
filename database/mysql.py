from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.logger import logger
from database.data import user_data, role_data, menu_data, user_role_data, role_menu_data, college_data, major_data, \
    classes_data, college_major_classes_data, student_classes_data
from models import User, Role, Menu, User_Role, Role_Menu, College, Major, Classes, College_Major_Classes, \
    Student_Classes
from models.base import Base

engine = create_engine(
    url=settings.MYSQL_URI,
    echo=settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,  # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
    pool_recycle=3600,
    # 设置隔离级别：READ COMMITTED | READ UNCOMMITTED | REPEATABLE READ | SERIALIZABLE | AUTOCOMMIT
    isolation_level='READ UNCOMMITTED'
)

localSession = sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)


def get_db():
    try:
        db = localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()


def create_db():
    try:
        Base.metadata.create_all(engine)
        logger.success('表结构配置成功')
    except Exception as e:
        logger.error(f'表结构创建失败 -- 错误信息如下:\n{e}')
    finally:
        engine.dispose()


def drop_db():
    try:
        Base.metadata.drop_all(engine)
        logger.success('表结构删除成功')
    except Exception as e:
        logger.error(f'表结构删除失败 -- 错误信息如下:\n{e}')
    finally:
        engine.dispose()


def init_data():
    try:
        engine.execute(User.__table__.insert(), [user for user in user_data])
        engine.execute(Role.__table__.insert(), [role for role in role_data])
        engine.execute(Menu.__table__.insert(), [menu for menu in menu_data])
        engine.execute(User_Role.__table__.insert(), [ur for ur in user_role_data])
        engine.execute(Role_Menu.__table__.insert(), [rm for rm in role_menu_data])
        engine.execute(College.__table__.insert(), [college for college in college_data])
        engine.execute(Major.__table__.insert(), [major for major in major_data])
        engine.execute(Classes.__table__.insert(), [classes for classes in classes_data])
        engine.execute(College_Major_Classes.__table__.insert(), [cmc for cmc in college_major_classes_data])
        engine.execute(Student_Classes.__table__.insert(), [sc for sc in student_classes_data])
        logger.success('初始化表数据成功')
    except Exception as e:
        logger.error(f'初始化表数据失败 -- 错误信息如下:\n{e}')
    finally:
        engine.dispose()


def init_db():
    # 删除表和数据
    drop_db()
    # 创建表结构
    create_db()
    # 初始化表数据
    init_data()
