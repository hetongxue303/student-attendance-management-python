import typing

from fastapi.encoders import jsonable_encoder
from pydantic.generics import GenericModel
from starlette import status
from starlette.responses import JSONResponse

T = typing.TypeVar("T")


class Result(GenericModel, typing.Generic[T]):
    code: int | None = status.HTTP_200_OK
    message: str | None = '请求成功'
    content: T | None = None


def JSONResult(
        *,
        code: int = status.HTTP_200_OK,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        message: str = '失败',
        data: typing.Any | None = None
):
    return JSONResponse(
        status_code=code,
        headers=headers,
        content={'code': code, 'message': message, 'data': jsonable_encoder(data)}
    )
