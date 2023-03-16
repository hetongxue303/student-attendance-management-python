from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import QueryException, UpdateException, DeleteException, InsertException
from filter.menu import filter_menu_to_tree
from models import Menu, Role_Menu
from schemas.menu import VOMenu, VOMenuTree
from schemas.result import Result, Page

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VOMenu]], summary='获取所有菜单')
async def get_all():
    try:
        return Result(content=db.query(Menu).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/role_id/{role_id}', response_model=Result[list[VOMenu]], summary='获取菜单(通过角色ID)')
async def get_all(role_id: int):
    try:
        role_menus = db.query(Role_Menu).filter(Role_Menu.role_id == role_id).all()
        rms: list[int] = []
        for rm in role_menus:
            rms.append(rm.menu_id)
        return Result(content=db.query(Menu).filter(Menu.menu_id.in_(rms)).all(), message='查询成功')
    except:
        raise QueryException(code=400, message='查询失败')


@router.get('/list/tree', response_model=Result[list[VOMenuTree]], summary='获取所有菜单(树)')
async def get_tree():
    try:
        return Result(content=filter_menu_to_tree(db.query(Menu).all()), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[VOMenu]]], summary='获取所有菜单(分页)')
async def get_page(page: int, size: int, menu_title: str = None):
    try:
        if menu_title:
            total = db.query(Menu).filter(Menu.menu_title.like('%{0}%'.format(menu_title))).count()
            record = db.query(Menu).filter(Menu.menu_title.like('%{0}%'.format(menu_title))).limit(
                size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        total = db.query(Menu).count()
        record = db.query(Menu).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加菜单')
async def insert(data: VOMenu):
    try:
        db.add(Menu(parent_id=data.parent_id, menu_title=data.menu_title, menu_type=data.menu_type.__str__(),
                    router_name=data.router_name, router_path=data.router_path, component=data.component,
                    sort=data.sort, icon=data.icon, permission=data.permission, sub_count=data.sub_count,
                    is_show='1' if data.is_show else '0', is_sub='1' if data.is_sub else '0',
                    is_status='1' if data.is_status else '0',
                    description=None if data.description == '' or data.description is None else data.description))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除菜单')
async def delete(id: int):
    try:
        db.query(Menu).filter(Menu.menu_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除菜单(批量)')
async def batch_delete(data: list[int]):
    try:
        db.query(Menu).filter(Menu.menu_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改菜单')
async def update(data: VOMenu):
    try:
        raw = db.query(Menu).filter(Menu.menu_id == data.menu_id).first()
        raw.parent_id = data.parent_id
        raw.menu_title = data.menu_title
        raw.menu_type = data.menu_type.__str__()
        raw.router_name = data.router_name
        raw.router_path = data.router_path
        raw.component = data.component
        raw.sort = data.sort
        raw.icon = data.icon
        raw.permission = data.permission
        raw.sub_count = data.sub_count
        raw.is_show = '1' if data.is_show else '0'
        raw.is_sub = '1' if data.is_sub else '0'
        raw.is_status = '1' if data.is_status else '0'
        raw.description = data.description
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
