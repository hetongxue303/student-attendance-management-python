from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.logger import logger
from models.base import Base

engine = create_engine(
    url=settings.MYSQL_URI,
    echo=settings.MYSQL_ECHO,
    pool_pre_ping=True,
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
