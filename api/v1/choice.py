from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import UpdateException, DeleteException, InsertException, QueryException
from models import Choice, Course
from schemas.choice import VOChoice
from schemas.result import Result, Page
from schemas.token import VOLogin
from utils.redis import get_userinfo

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VOChoice]], summary='获取所有选课')
async def get_all():
    try:
        return Result(content=db.query(Choice).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[VOChoice]]], summary='获取所有选课(分页)')
async def get_page(page: int, size: int):
    try:
        total = db.query(Choice).count()
        record = db.query(Choice).limit(size).offset((page - 1) * size).all()
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加选课')
async def insert(data: VOChoice):
    userinfo: VOLogin = await get_userinfo()
    # 判断是否重复选择
    if db.query(Choice).filter(Choice.user_id == userinfo.user_id,
                               Choice.course_id == data.course_id,
                               Choice.choice_status != '3').all():
        raise InsertException(message='你已选过该课程，无需重复选择')
    course = db.query(Course).filter(Course.course_id == data.course_id).first()
    # 判断课程是否还有数量
    if course.count == course.selection:
        raise InsertException(message='该课程人数已满')
    try:
        # 数量减一
        course.selection = course.selection + 1
        db.add(Choice(user_id=userinfo.user_id, course_id=data.course_id))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除选课')
async def delete(id: int):
    try:
        db.query(Choice).filter(Choice.choice_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除选课(批量)')
async def batch_delete(data: list[int]):
    try:
        db.query(Choice).filter(Choice.choice_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改选课')
async def update(data: VOChoice):
    try:
        raw = db.query(Choice).filter(Choice.choice_id == data.choice_id).first()
        raw.user_id = data.user_id
        raw.course_id = data.course_id
        raw.score = data.score
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()


@router.put('/update/score', response_model=Result, summary='修改选课成绩')
async def update(data: VOChoice):
    try:
        raw = db.query(Choice).filter(Choice.choice_id == data.choice_id).first()
        print(raw.choice_id)
        raw.score = data.score
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()


@router.put('/update/status', response_model=Result, summary='修改选课状态')
async def update(data: VOChoice):
    try:
        raw = db.query(Choice).filter(Choice.choice_id == data.choice_id).first()
        raw.choice_status = data.choice_status.__str__()
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
