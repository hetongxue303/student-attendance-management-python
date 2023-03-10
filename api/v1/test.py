import typing

from fastapi import APIRouter

router = APIRouter()


@router.get('/test', response_model=typing.Any, summary='测试接口')
async def test():
    return 'test success'
