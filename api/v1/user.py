from fastapi import APIRouter
from sqlalchemy.orm import Session

from core.security import get_password_hash
from database.mysql import get_db
from exception.custom import QueryException, UpdateException, DeleteException, InsertException
from models import User, User_Role, Student_Classes, Choice, Attendance, Check
from schemas.check import VOCheck
from schemas.result import Result, Page
from schemas.user import BOUser, DTOUser, VOChoiceStudent

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[BOUser]], summary='获取所有用户')
async def get_all():
    try:
        return Result(content=db.query(User).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list/byAttendanceId', response_model=Result[Page[list[VOChoiceStudent]]], summary='获取所有签到学生')
async def get_all_by_attendance_id(page: int, size: int, attendance_id: int = None, status: bool = None):
    try:
        # 查询考勤信息
        attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()

        # 通过考勤信息查询选课的学生有哪些
        data = db.query(Choice).filter(Choice.course_id == attendance.course_id, Choice.choice_status == '1').all()

        # 设置total
        total: int = 0
        for i in data:
            tmp = db.query(Check).filter(Check.user_id == i.user.user_id,
                                         Check.attendance_id == attendance_id,
                                         Check.course_id == i.course_id).first()
            if status and tmp:
                total = total + 1
            if not status and not tmp:
                total = total + 1
                
        # 设置数据
        choices = db.query(Choice).filter(Choice.course_id == attendance.course_id, Choice.choice_status == '1').limit(
            size).offset((page - 1) * size).all()
        record: list[VOChoiceStudent] = []
        if choices:
            for item in choices:
                user: User | BOUser = db.query(User).filter(User.user_id == item.user_id).first()
                check: Check | VOCheck = db.query(Check).filter(Check.user_id == user.user_id,
                                                                Check.attendance_id == attendance_id,
                                                                Check.course_id == item.course_id).first()
                if status and check:
                    record.append(VOChoiceStudent(user=user, is_checked=True, check_time=check.check_time))
                if not check and not status:
                    record.append(VOChoiceStudent(user=user, is_checked=False))
            return Result(content=Page(total=total, record=record), message='查询成功')
        return Result(content=Page(total=0, record=[]), message='查询成功')
    except:
        raise QueryException()


@router.get('/list/courseById', response_model=Result[Page[list[BOUser]]], summary='获取学生(我的、分页)')
async def get_all(page: int, size: int, course_id: int = None):
    try:
        choice = db.query(Choice).filter(Choice.choice_id == course_id).distinct().all()
        if not choice:
            return Result(content=Page(total=0, record=[]), message='查询成功')
        ids = [item.user_id for item in choice]
        total = db.query(User).filter(User.user_id.in_(ids)).count()
        record = db.query(User).filter(User.user_id.in_(ids)).limit(size).offset(
            (page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
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


@router.get('/list', response_model=Result[Page[list[DTOUser]]], summary='获取所有用户(分页)')
async def get_page(page: int, size: int, username: str = None, real_name: str = None):
    try:
        if real_name and username:
            total = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name)),
                                          User.username.like('%{0}%'.format(username))).count()
            temp = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name)),
                                         User.username.like('%{0}%'.format(username))).limit(size).offset(
                (page - 1) * size).all()
            record: list[DTOUser] = []
            for item in temp:
                tmp: DTOUser | User = item
                tmp.role_id = db.query(User_Role).filter(User_Role.user_id == item.user_id).first().role_id
                record.append(tmp)
            return Result(content=Page(total=total, record=record), message='查询成功')

        if real_name:
            total = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name))).count()
            temp = db.query(User).filter(User.real_name.like('%{0}%'.format(real_name))).limit(
                size).offset((page - 1) * size).all()
            record: list[DTOUser] = []
            for item in temp:
                tmp: DTOUser | User = item
                tmp.role_id = db.query(User_Role).filter(User_Role.user_id == item.user_id).first().role_id
                record.append(tmp)
            return Result(content=Page(total=total, record=record), message='查询成功')

        if username:
            total = db.query(User).filter(User.username.like('%{0}%'.format(username))).count()
            temp = db.query(User).filter(User.username.like('%{0}%'.format(username))).limit(
                size).offset((page - 1) * size).all()
            record: list[DTOUser] = []
            for item in temp:
                tmp: DTOUser | User = item
                tmp.role_id = db.query(User_Role).filter(User_Role.user_id == item.user_id).first().role_id
                record.append(tmp)
            return Result(content=Page(total=total, record=record), message='查询成功')

        total = db.query(User).count()
        record = db.query(User).limit(size).offset((page - 1) * size).all()
        for item in record:
            item.role_id = db.query(User_Role).filter(User_Role.user_id == item.user_id).first().role_id
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加用户')
async def insert(data: DTOUser):
    if db.query(User).filter(User.username == data.username).first():
        raise InsertException(message='用户名已存在')
    try:
        user = User(username=data.username, real_name=data.real_name, gender=data.gender.__str__(),
                    is_status='1' if data.is_status else '0', password=get_password_hash(data.password),
                    description=None if data.description == '' or data.description is None else data.description)
        db.add(user)
        db.commit()
        db.add(User_Role(user_id=user.user_id, role_id=data.role_id))
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
async def update(data: DTOUser):
    try:
        raw = db.query(User).filter(User.user_id == data.user_id).first()
        temp = db.query(User_Role).filter(User_Role.user_id == data.user_id).first()
        raw.real_name = data.real_name
        raw.gender = data.gender.__str__()
        raw.is_status = '1' if data.is_status else '0'
        raw.is_admin = '1' if data.is_admin else '0'
        raw.description = data.description
        temp.role_id = data.role_id
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
