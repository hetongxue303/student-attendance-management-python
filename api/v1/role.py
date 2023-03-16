from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import QueryException, UpdateException, DeleteException, InsertException
from models import Role, Role_Menu, User_Role
from schemas.result import Result, Page
from schemas.role import VORole, BORole

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
async def insert(data: BORole):
    role: VORole = data.role
    ids: list[int] = data.menu_ids
    if db.query(Role).filter(Role.role_name == role.role_name).first():
        raise InsertException(message='角色名称重复')
    if db.query(Role).filter(Role.role_code == role.role_code).first():
        raise InsertException(message='角色名称标识')
    try:
        role_info = Role(role_name=role.role_name, role_code=role.role_code, is_status='1' if role.is_status else '0',
                         description=None if role.description == '' or role.description is None else role.description)
        db.add(role_info)
        db.commit()
        for id in ids:
            db.add(Role_Menu(role_id=role_info.role_id, menu_id=id))
            db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除角色')
async def delete(id: int):
    if db.query(User_Role).filter(User_Role.role_id == id).all():
        raise DeleteException(message='该角色列表下还有用户，不能删除！')
    try:
        rm = db.query(Role_Menu).filter(Role_Menu.role_id == id).all()
        if rm:
            db.delete(rm)
        db.query(Role).filter(Role.role_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除角色(批量)')
async def batch_delete(data: list[int]):
    if db.query(User_Role).filter(User_Role.role_id.in_(data)).all():
        raise DeleteException(message='有角色列表下还有用户，不能删除！')
    try:
        rm = db.query(Role_Menu).filter(Role_Menu.role_id.in_(data)).all()
        if rm:
            db.delete(rm)
        db.query(Role).filter(Role.role_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改角色')
async def update(data: BORole):
    role: VORole = data.role
    ids: list[int] = data.menu_ids
    temp_name_id = db.query(Role).filter(Role.role_id == role.role_id).first()
    if db.query(Role).filter(Role.role_name == role.role_name).first() and temp_name_id.role_name != role.role_name:
        raise InsertException(message='角色名称重复')
    if db.query(Role).filter(Role.role_code == role.role_code).first() and temp_name_id.role_code != role.role_code:
        raise InsertException(message='角色标识重复')
    try:
        raw = db.query(Role).filter(Role.role_id == role.role_id).first()
        raw.role_name = role.role_name
        raw.role_code = role.role_code
        raw.is_status = '1' if role.is_status else '0'
        raw.description = role.description
        ids_all = [i.menu_id for i in db.query(Role_Menu).filter(Role_Menu.role_id == role.role_id).all()]
        add_ids = [i for i in (ids + ids_all) if i not in ids_all]
        delete_ids = [i for i in ids_all if i not in [x for x in ids if x in ids_all]]
        if delete_ids:
            db.query(Role_Menu).filter(Role_Menu.menu_id.in_(delete_ids), Role_Menu.role_id == role.role_id).delete()
        for id in add_ids:
            db.add(Role_Menu(role_id=role.role_id, menu_id=id))
        if add_ids or delete_ids:
            raw.update_time = func.now()
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()


@router.put('/update/status', response_model=Result, summary='修改角色状态')
async def update(data: VORole):
    try:
        raw = db.query(Role).filter(Role.role_id == data.role_id).first()
        raw.is_status = '1' if data.is_status else '0'
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
