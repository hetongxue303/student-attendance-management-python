import os
from typing import List

from loguru import logger

"""日志配置"""
LOGGER_DIR: str = 'logs'  # 日志文件夹名
LOGGER_NAME: str = '{time:YYYY-MM-DD_HH-mm-ss}.log'  # 日志文件名 (时间格式)
LOGGER_LEVEL: str = 'DEBUG'  # 日志等级: ['DEBUG' | 'INFO']
LOGGER_ROTATION: str = '12:00'  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
LOGGER_RETENTION: str = '1 days'  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]
LOGGER_ENCODING: str = 'utf-8'  # 全局编码
LOGGER_MAX: int = 3  # 最大文件数


def logger_file() -> str:
    log_path: str = create_dir(LOGGER_DIR)
    file_list: List[str] = os.listdir(log_path)
    if len(file_list) > LOGGER_MAX:
        os.remove(os.path.join(log_path, file_list[0]))
    return os.path.join(log_path, LOGGER_NAME)


def create_dir(file_name: str) -> str:
    current_path = os.path.dirname(__file__)  # 获取当前文件夹
    parent_path = os.path.abspath(os.path.join(current_path, ".."))  # 获取当前文件夹的上一层文件
    path = parent_path + os.sep + file_name + os.sep  # 拼接日志文件夹的路径
    os.makedirs(path, exist_ok=True)  # 如果文件夹不存在就创建
    return path


logger.add(
    logger_file(),
    encoding=LOGGER_ENCODING,
    level=LOGGER_LEVEL,
    rotation=LOGGER_ROTATION,
    retention=LOGGER_RETENTION,
    enqueue=True
)
