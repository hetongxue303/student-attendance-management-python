from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import QueryException, DeleteException, InsertException, UpdateException
from models import Major
from schemas.major import VOMajor
from schemas.result import Result, Page

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VOMajor]], summary='获取所有专业')
async def get_all():
    try:
        return Result(content=db.query(Major).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[VOMajor]]], summary='获取所有专业(分页)')
async def get_page(page: int, size: int, major_name: str = None):
    try:
        if major_name:
            total = db.query(Major).filter(Major.major_name.like('%{0}%'.format(major_name))).count()
            record = db.query(Major).filter(Major.major_name.like('%{0}%'.format(major_name))).limit(size).offset(
                (page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        total = db.query(Major).count()
        record = db.query(Major).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.get('/college_id/{college_id}', response_model=Result[list[VOMajor]], summary='获取专业(学院ID)')
async def get_major_by_college_id(college_id: int):
    try:
        return Result(content=db.query(Major).filter(Major.college_id == college_id).all(), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='新增专业')
async def insert(data: VOMajor):
    try:
        db.add(Major(major_name=data.major_name, college_id=data.college_id,
                     description=None if data.description == '' or data.description is None else data.description))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除专业')
async def delete(id: int):
    try:
        db.query(Major).filter(Major.major_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除专业(批量)')
async def batch_delete(data: list[int]):
    try:
        db.query(Major).filter(Major.major_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改专业')
async def update(data: VOMajor):
    try:
        raw = db.query(Major).filter(Major.major_id == data.major_id).first()
        raw.major_name = data.major_name
        raw.description = data.description
        raw.college_id = data.college_id
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
