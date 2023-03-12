from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import QueryException, UpdateException, DeleteException, InsertException
from models import User
from schemas.result import Result, Page
from schemas.user import BOUser, VOUser

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[BOUser]], summary='获取所有用户')
async def get_all():
    try:
        return Result(content=db.query(User).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[BOUser]]], summary='获取所有用户(分页)')
async def get_page(page: int, size: int, real_name: str = None):
    try:
        if real_name:
            total = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name))).count()
            record = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name))).limit(
                size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        total = db.query(User).count()
        record = db.query(User).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加用户')
async def insert(data: VOUser):
    try:
        db.add(User(username=data.username, real_name=data.real_name, gender=data.gender,
                    description=None if data.description == '' or data.description is None else data.description))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除用户')
async def delete(id: int):
    try:
        db.query(User).filter(User.user_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除用户(批量)')
async def batch_delete(data: list[int]):
    try:
        db.query(User).filter(User.user_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改用户')
async def update(data: BOUser):
    try:
        print(data)
        raw = db.query(User).filter(User.user_id == data.user_id).first()
        raw.real_name = data.real_name
        raw.gender = data.gender.__str__()
        raw.is_status = '1' if data.is_status else '0'
        raw.is_admin = '1' if data.is_admin else '0'
        raw.description = data.description
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
