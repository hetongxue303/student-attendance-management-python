from pydantic import BaseSettings, AnyHttpUrl

app_desc = """
    🎉 用户登录 🎉
    ✨ 默认账号: admin ✨
    ✨ 默认密码: 123456 ✨
"""


class Settings(BaseSettings):
    # 基础配置
    APP_TITLE: str = '学生考勤管理系统'  # 应用标题
    APP_API_PREFIX: str = ''  # 接口前缀
    APP_DEBUG: bool = True  # 是否debug
    APP_CORS: bool = True  # 是否跨域
    APP_DESC: str = app_desc  # 项目描述
    APP_VERSION: str = '0.1'  # 版本
    APP_STATIC_DIR: str = 'static'  # 静态文件目录
    APP_GLOBAL_ENCODING: str = 'utf-8'  # 全局编码
    APP_CORS_ORIGINS: list[AnyHttpUrl] = ['http://127.0.0.1:3000', 'http://127.0.0.1:5179']  # 跨域请求(列表)
    APP_IS_RELOAD: bool = True  # 是否热部署

    # 数据源配置
    REDIS_URL: str = 'redis://127.0.0.1'  # redis url
    REDIS_PORT: int = 6379  # redis端口
    REDIS_DB: int = 1  # redis 数据库
    REDIS_DEFAULT_EXPIRE: int = 30 * 60 * 1000  # redis默认过期时间
    MYSQL_URI: str = 'mysql+pymysql://root:123456@127.0.0.1:3306/student_attendance_management?charset=utf8'  # mysql
    MYSQL_ECHO: bool = True  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)
    IS_INIT_MYSQL_DATA: bool = False  # 是否初始化表数据及结构

    # jwt配置
    JWT_SAVE_KEY = 'authorization'
    JWT_ALGORITHM: str = 'HS256'
    # JWT_SECRET_KEY: str = secrets.token_urlsafe(32)  # 密钥(每次重启服务密钥都会改变, token解密失败导致过期, 可设置为常量)
    JWT_SECRET_KEY: str = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    JWT_EXPIRE: int = 30 * 60 * 1000  # token过期时间: 30分钟 单位：毫秒
    JWT_IS_BEARER: bool = True  # 开启Bearer

    class Config:
        env_fil: str = '.env'
        case_sensitive: bool = True  # 区分大小写


settings = Settings()
