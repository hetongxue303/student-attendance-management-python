from fastapi import APIRouter
from sqlalchemy.orm import Session

from core.security import get_password_hash
from database.mysql import get_db
from exception.custom import QueryException, UpdateException, DeleteException, InsertException
from models import User, User_Role, Student_Classes
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


@router.get('/list/teacher', response_model=Result[list[BOUser]], summary='获取所有教师')
async def get_by_username(username: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        temp = db.query(User_Role).filter(User_Role.role_id == 2).all()
        ids = [item.user_id for item in temp]
        if bool(int(user.is_admin)):
            return Result(content=db.query(User).filter(User.user_id.in_(ids)).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[BOUser]]], summary='获取所有用户(分页)')
async def get_page(page: int, size: int, username: str = None, real_name: str = None):
    try:
        if real_name and username:
            total = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name)),
                                          User.username.like('%{0}%'.format(username))).count()
            record = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name)),
                                           User.username.like('%{0}%'.format(username))).limit(size).offset(
                (page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        if real_name:
            total = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name))).count()
            record = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name))).limit(
                size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        if username:
            total = db.query(User).filter(User.username.like('%{0}%'.format(username))).count()
            record = db.query(User).filter(User.username.like('%{0}%'.format(username))).limit(
                size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        total = db.query(User).count()
        record = db.query(User).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加用户')
async def insert(data: VOUser):
    if db.query(User).filter(User.username == data.username).first():
        raise InsertException(message='用户名已存在')
    try:
        db.add(User(username=data.username, real_name=data.real_name, gender=data.gender.__str__(),
                    is_status='1' if data.is_status else '0', password=get_password_hash(data.password),
                    description=None if data.description == '' or data.description is None else data.description))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除用户')
async def delete(id: int):
    try:
        ur = db.query(User_Role).filter(User_Role.user_id == id).all()
        if ur:
            db.delete(ur)
        sc = db.query(Student_Classes).filter(Student_Classes.user_id == id).all()
        db.delete(sc)
        db.query(User).filter(User.user_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除用户(批量)')
async def batch_delete(data: list[int]):
    try:
        ur = db.query(User_Role).filter(User_Role.user_id.in_(data)).all()
        if ur:
            db.delete(ur)
        sc = db.query(Student_Classes).filter(Student_Classes.user_id.in_(data)).all()
        if sc:
            db.delete(sc)
        db.query(User).filter(User.user_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改用户')
async def update(data: BOUser):
    try:
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
