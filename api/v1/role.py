from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import QueryException, UpdateException, DeleteException, InsertException
from models import Role
from schemas.result import Result, Page
from schemas.role import VORole

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VORole]], summary='获取所有角色')
async def get_all():
    try:
        return Result(content=db.query(Role).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[VORole]]], summary='获取所有角色(分页)')
async def get_page(page: int, size: int, role_name: str = None):
    try:
        if role_name:
            total = db.query(Role).filter(Role.role_name.like('%{0}%'.format(role_name))).count()
            record = db.query(Role).filter(Role.role_name.like('%{0}%'.format(role_name))).limit(
                size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        total = db.query(Role).count()
        record = db.query(Role).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加角色')
async def insert(data: VORole):
    try:
        db.add(Role(role_name=data.role_name, role_code=data.role_code, is_status='1' if data.is_status else '0',
                    description=None if data.description == '' or data.description is None else data.description))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除角色')
async def delete(id: int):
    try:
        db.query(Role).filter(Role.role_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除角色(批量)')
async def batch_delete(data: list[int]):
    try:
        db.query(Role).filter(Role.role_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改角色')
async def update(data: VORole):
    try:
        raw = db.query(Role).filter(Role.role_id == data.role_id).first()
        raw.role_name = data.role_name
        raw.role_code = data.role_code
        raw.is_status = '1' if data.is_status else '0'
        raw.description = data.description
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
