from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import UpdateException, DeleteException, InsertException, QueryException
from models import Choice, Course, Teacher_Course
from schemas.choice import VOChoice, VOChoiceBatch
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
async def get_page(page: int, size: int, course_name: str = None):
    try:
        # 只能查询自己的课程的选课 管理员除外
        userinfo: VOLogin = await get_userinfo()
        # 管理员
        if userinfo.is_admin:
            if course_name:
                course = db.query(Course).filter(Course.course_name.like('%{0}%'.format(course_name)))
                if course:
                    ids = [item.course_id for item in course]
                    total = db.query(Choice).filter(Choice.choice_status == '-1', Choice.course_id.in_(ids)).count()
                    record = db.query(Choice).filter(Choice.choice_status == '-1', Choice.course_id.in_(ids)).limit(
                        size).offset((page - 1) * size).all()
                    return Result(content=Page(total=total, record=record), message='查询成功')
                return Result(content=Page(total=0, record=[]), message='查询成功')
            total = db.query(Choice).filter(Choice.choice_status == '-1').count()
            record = db.query(Choice).filter(Choice.choice_status == '-1').limit(size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')

        # 教师
        tc = db.query(Teacher_Course).filter(Teacher_Course.user_id == userinfo.user_id).all()
        if tc:
            if course_name:
                course_ids = [item.course_id for item in tc]
                course = db.query(Course).filter(Course.course_name.like('%{0}%'.format(course_name)),
                                                 Course.course_id.in_(course_ids))
                if course:
                    ids = [item.course_id for item in course]
                    total = db.query(Choice).filter(Choice.choice_status == '-1', Choice.course_id.in_(ids)).count()
                    record = db.query(Choice).filter(Choice.choice_status == '-1', Choice.course_id.in_(ids)).limit(
                        size).offset((page - 1) * size).all()
                    return Result(content=Page(total=total, record=record), message='查询成功')
                return Result(content=Page(total=0, record=[]), message='查询成功')

            ids = [item.course_id for item in tc]
            total = db.query(Choice).filter(Choice.choice_status == '-1', Choice.course_id.in_(ids)).count()
            record = db.query(Choice).filter(Choice.choice_status == '-1', Choice.course_id.in_(ids)).limit(
                size).offset((page - 1) * size).all()
            return Result(content=Page(total=total, record=record), message='查询成功')
        return Result(content=Page(total=0, record=[]), message='查询成功')

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
        # 选课人数加一
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
async def update_score(data: VOChoice):
    try:
        raw = db.query(Choice).filter(Choice.choice_id == data.choice_id).first()
        raw.score = data.score
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()


@router.put('/update/status', response_model=Result, summary='修改选课状态')
async def update_status(data: VOChoice):
    try:
        raw = db.query(Choice).filter(Choice.choice_id == data.choice_id).first()
        raw.choice_status = data.choice_status.__str__()
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()


@router.put('/update/status/batch', response_model=Result, summary='修改选课状态(批量)')
async def batch_update_batch(data: VOChoiceBatch):
    try:
        print(data)
        temp = db.query(Choice).filter(Choice.choice_id.in_(data.ids)).all()
        for item in temp:
            item.choice_status = data.choice_status.__str__()
            db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
