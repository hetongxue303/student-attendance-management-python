"""
自定义异常
@Author:何同学
"""


class UserNotFoundException(Exception):
    def __init__(self, message: str = '用户名或密码错误'):
        self.message = message


class UserPasswordException(Exception):
    def __init__(self, message: str = '密码错误'):
        self.message = message


class CaptchaException(Exception):
    def __init__(self, message: str = '验证码错误'):
        self.message = message


class UnauthorizedException(Exception):
    def __init__(self, message: str = '您还未登录,请先登录!'):
        self.message = message


class JwtVerifyException(Exception):
    def __init__(self, message: str = 'JWT解析失败'):
        self.message = message


class SecurityScopeException(Exception):
    def __init__(self, message: str = '请选择作用域！', code: int = 401, headers: dict = None):
        self.message = message
        self.headers = headers
        self.code = code


class InsertException(Exception):
    def __init__(self, message: str = '新增失败', code: int = 400, headers: dict = None):
        self.message = message
        self.headers = headers
        self.code = code


class DeleteException(Exception):
    def __init__(self, message: str = '删除失败', code: int = 400, headers: dict = None):
        self.message = message
        self.headers = headers
        self.code = code


class UpdateException(Exception):
    def __init__(self, message: str = '更新失败', code: int = 400, headers: dict = None):
        self.message = message
        self.headers = headers
        self.code = code


class QueryException(Exception):
    def __init__(self, message: str = '查询失败', code: int = 400, headers: dict = None):
        self.message = message
        self.headers = headers
        self.code = code
