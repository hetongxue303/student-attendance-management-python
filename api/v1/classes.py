from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import QueryException, InsertException, DeleteException, UpdateException
from models import Classes
from schemas.classes import VOClasses
from schemas.result import Result, Page

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VOClasses]], summary='获取所有班级')
async def get_all():
    try:
        return Result(content=db.query(Classes).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[list[VOClasses]], summary='获取所有班级(分页)')
async def get_page(page: int, size: int):
    try:
        total = db.query(Classes).count()
        record = db.query(Classes).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='新增班级')
async def add(data: VOClasses):
    try:
        db.add(Classes(classes_name=data.classes_name, college_id=data.college_id, major_id=data.major_id,
                       description=None if data.description == '' or data.description is None else data.description))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除班级')
async def add(id: int):
    try:
        db.query(Classes).filter(Classes.classes_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除班级(批量)')
async def add(data: list[int]):
    try:
        db.query(Classes).filter(Classes.classes_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改班级')
async def add(data: VOClasses):
    try:
        raw = db.query(Classes).filter(Classes.classes_id == data.classes_id).first()
        raw.classes_name = data.classes_name
        raw.college_id = data.college_id
        raw.major_id = data.major_id
        raw.description = data.description
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
