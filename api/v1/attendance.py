from fastapi import APIRouter
from sqlalchemy.orm import Session

from database.mysql import get_db
from exception.custom import UpdateException, DeleteException, InsertException, QueryException
from models.attendance import Attendance
from schemas.attendance import VOAttendance, BOAttendance
from schemas.result import Result, Page

router = APIRouter()
db: Session = next(get_db())


@router.get('/list/all', response_model=Result[list[VOAttendance]], summary='获取所有签到记录')
async def get_all():
    try:
        return Result(content=db.query(Attendance).all(), message='查询成功')
    except:
        raise QueryException()


@router.get('/list', response_model=Result[Page[list[BOAttendance]]], summary='获取所有签到记录(分页)')
async def get_page(page: int, size: int, status: int = None):
    try:
        total = db.query(Attendance).filter(Attendance.status == status.__str__()).count()
        record = db.query(Attendance).filter(Attendance.status == status.__str__()).limit(size).offset(
            (page - 1) * size).all()
        for item in record:
            # TODO 待完善
            item.checked_count = 1
        return Result(content=Page(total=total, record=record), message='查询成功')
    except:
        raise QueryException()


@router.post('/add', response_model=Result, summary='添加签到记录')
async def insert(data: VOAttendance):
    try:
        db.add(Attendance(user_id=data.user_id, course_id=data.course_id, time=data.time))
        db.commit()
        return Result(message='添加成功')
    except:
        db.rollback()
        raise InsertException()


@router.delete('/delete/{id}', response_model=Result, summary='删除签到记录')
async def delete(id: int):
    try:
        db.query(Attendance).filter(Attendance.attendance_id == id).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/delete/batch', response_model=Result, summary='删除签到记录(批量)')
async def batch_delete(data: list[int]):
    try:
        db.query(Attendance).filter(Attendance.attendance_id.in_(data)).delete()
        db.commit()
        return Result(message='删除成功')
    except:
        db.rollback()
        raise DeleteException()


@router.put('/update', response_model=Result, summary='修改签到记录')
async def update(data: VOAttendance):
    try:
        raw = db.query(Attendance).filter(Attendance.attendance_id == data.attendance_id).first()
        raw.user_id = data.user_id
        raw.course_id = data.course_id
        raw.time = data.time
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()


@router.put('/update/status', response_model=Result, summary='更新签到状态')
async def update(data: VOAttendance):
    try:
        raw = db.query(Attendance).filter(Attendance.attendance_id == data.attendance_id).first()
        raw.status = '1'
        db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
    raise UpdateException()


@router.put('/update/status/batch', response_model=Result, summary='更新签到状态(批量)')
async def update(data: list[int]):
    try:
        raw = db.query(Attendance).filter(Attendance.attendance_id.in_(data)).all()
        for item in raw:
            item.status = '1'
            db.commit()
        return Result(message='修改成功')
    except:
        db.rollback()
        raise UpdateException()
