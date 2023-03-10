from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import UpdateException, DeleteException, InsertException, QueryException
from models import College
from schemas.college import VOCollege
from schemas.result import Result, Page

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VOCollege]], summary='获取所有学院')
async def get_all():
    try:
        return Result(content=db.query(College).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[VOCollege]]], summary='获取所有学院(分页)')
async def get_page(page: int, size: int):
    try:
        total = db.query(College).count()
        record = db.query(College).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.put('/add', response_model=Result, summary='添加学院')
async def add(data: VOCollege):
    try:
        db.add(College(college_name=data.college_name,
                       description=None if data.description == '' or data.description is None else data.description))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除学院')
async def add(id: int):
    try:
        db.query(College).filter(College.college_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除学院(批量)')
async def add(data: list[int]):
    try:
        db.query(College).filter(College.college_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改学院')
async def add(data: VOCollege):
    try:
        raw = db.query(College).filter(College.college_id == data.college_id).first()
        raw.college_name = data.college_name
        raw.description = data.description
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
