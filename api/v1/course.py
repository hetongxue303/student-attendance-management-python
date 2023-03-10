from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import QueryException, UpdateException, DeleteException, InsertException
from models import Course, User, User_Course
from schemas.course import VOCourse, BOCourse
from schemas.result import Result, Page
from schemas.token import VOLogin
from utils.redis import get_userinfo

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VOCourse]], summary='获取所有课程')
async def get_all():
    try:
        return Result(content=db.query(Course).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list/me', response_model=Result[Page[list[VOCourse]]], summary='我的课程(分页)')
async def get_course_me(page: int, size: int, username: str, course_name: str = None):
    try:
        user: User = db.query(User).filter(User.username == username).first()
        if course_name:
            if bool(int(user.is_admin)):
                total = db.query(Course).filter(Course.course_name.like('%{0}%'.format(course_name))).count()
                record = db.query(Course).filter(Course.course_name.like('%{0}%'.format(course_name))).limit(
                    size).offset((page - 1) * size).all()
                return Result(content=Page(total=total, record=record), message='查询成功')
            temp: list = db.query(User_Course).filter(User_Course.user_id == user.user_id).all()
            ids: list[int] = [item.course_id for item in temp]
            total = db.query(Course).filter(Course.course_id.in_(ids),
                                            Course.course_name.like('%{0}%'.format(course_name))).count()
            record = db.query(Course).filter(Course.course_id.in_(ids),
                                             Course.course_name.like('%{0}%'.format(course_name))).limit(
                size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        if bool(int(user.is_admin)):
            total = db.query(Course).count()
            record = db.query(Course).limit(size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')
        temp: list = db.query(User_Course).filter(User_Course.user_id == user.user_id).all()
        ids: list[int] = [item.course_id for item in temp]
        total = db.query(Course).filter(Course.course_id.in_(ids)).count()
        record = db.query(Course).filter(Course.course_id.in_(ids)).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[VOCourse]]], summary='获取所有课程(分页)')
async def get_page(page: int, size: int, course_name: str = None):
    try:
        if course_name:
            total = db.query(Course).filter(Course.course_name.like('%{0}%'.format(course_name))).count()
            record = db.query(Course).filter(Course.course_name.like('%{0}%'.format(course_name))).limit(
                size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        total = db.query(Course).count()
        record = db.query(Course).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加课程')
async def insert(data: BOCourse):
    try:
        course = Course(course_name=data.course_name, college_id=data.college_id, major_id=data.major_id,
                        classes_id=data.classes_id, count=data.count, time=data.time,
                        description=None if data.description == '' or data.description is None else data.description)
        db.add(course)
        db.commit()
        db.add(User_Course(user_id=data.user_id, course_id=course.course_id))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除课程')
async def delete(id: int):
    try:
        userinfo: VOLogin = await get_userinfo()
        db.query(Course).filter(Course.course_id == id).delete()
        db.query(User_Course).filter(User_Course.course_id == id, User_Course.user_id == userinfo.user_id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除课程(批量)')
async def batch_delete(data: list[int]):
    try:
        db.query(Course).filter(Course.course_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改课程')
async def update(data: BOCourse):
    try:
        raw = db.query(Course).filter(Course.course_id == data.course_id).first()
        raw.course_name = data.course_name
        raw.college_id = data.college_id
        raw.major_id = data.major_id
        raw.classes_id = data.classes_id
        raw.count = data.count
        raw.time = data.time
        raw.description = data.description
        temp = db.query(User_Course).filter(User_Course.course_id == data.course_id).first()
        temp.user_id = data.user_id
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
