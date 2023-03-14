from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import UpdateException, DeleteException, InsertException, QueryException
from models import Check
from schemas.check import VOCheck
from schemas.result import Result, Page

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VOCheck]], summary='获取所有签到记录')
async def get_all():
    try:
        return Result(content=db.query(Check).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[VOCheck]]], summary='获取所有签到记录(分页)')
async def get_page(page: int, size: int):
    try:
        total = db.query(Check).count()
        record = db.query(Check).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加签到记录')
async def insert(data: VOCheck):
    try:
        db.add(Check(user_id=data.user_id, course_id=data.course_id))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除签到记录')
async def delete(id: int):
    try:
        db.query(Check).filter(Check.check_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除签到记录(批量)')
async def batch_delete(data: list[int]):
    try:
        db.query(Check).filter(Check.check_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改签到记录')
async def update(data: VOCheck):
    try:
        raw = db.query(Check).filter(Check.check_id == data.check_id).first()
        raw.user_id = data.user_id
        raw.course_id = data.course_id
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
