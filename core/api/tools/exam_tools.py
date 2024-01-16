from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from core.models.exam import Exam, ExamType
from sqlalchemy.engine import Result
from core.api.schemas.exams import ExamResponse, ExamCreate, ExamResponseWithEmployee, ExamCreated
import datetime

async def get_all_exams_by_id(session: AsyncSession, skip: int | None, limit: int | None, id: int) -> list[ExamResponse]:
    stmt = select(Exam).options(joinedload(Exam.exam_type)).where(Exam.employee_id == id).order_by(Exam.next_date.desc()).offset(skip).limit(limit)
    res: Result = await session.execute(stmt)
    exams: list[Exam] = res.scalars().all()
    result = []
    for item in exams:
        exam : Exam = item
        res: ExamResponse = ExamResponse(
            id = exam.id,
            exam_name = exam.exam_type.name,
            exam_type_id = exam.exam_type_id,
            date = exam.date,
            next_date = exam.next_date,
            protocol=exam.protocol,
            notation=exam.notation,
            place=exam.place
        )
        if exam.next_date - datetime.date.today() > datetime.timedelta(days=0):
            result.append(res)
    result.sort(key=lambda x: x.next_date - datetime.date.today(), reverse=False)
    return result

async def get_all_exams_from_db(skip: int, limit: int, session: AsyncSession) -> list[ExamResponseWithEmployee]:
    stmt = select(Exam).options(joinedload(Exam.exam_type), joinedload(Exam.employee)).offset(skip).limit(limit)
    res: Result = await session.execute(stmt)
    exams: list[Exam] = res.scalars().all()
    result = []
    for item in exams:
        exam : Exam = item
        res: ExamResponseWithEmployee = ExamResponseWithEmployee(
            id = exam.id,
            exam_name = exam.exam_type.name,
            exam_type_id = exam.exam_type_id,
            date = exam.date,
            next_date = exam.next_date,
            protocol=exam.protocol,
            notation=exam.notation,
            place=exam.place,
            employee=exam.employee.FIO,
            employee_id=exam.employee_id
        )
        result.append(res)
    return result

async def add_exam_in_db(employee_id: int, new_exam: ExamCreate,session: AsyncSession):
    exam = Exam()
    exam.exam_type_id = new_exam.exam_type_id
    exam.date = new_exam.date
    stmt = select(ExamType).where(ExamType.id == new_exam.exam_type_id)
    res: Result = await session.execute(stmt)
    exam_type: ExamType = res.scalar_one()
    if len(new_exam.next_date) == 0:
        exam.next_date = new_exam.date + datetime.timedelta(days=exam_type.period)
    else:
        exam.next_date = datetime.datetime.strptime(new_exam.next_date, "%Y-%m-%d") 
    exam.employee_id = employee_id
    exam.protocol = new_exam.protocol
    exam.notation = new_exam.notation
    exam.place = new_exam.place
    session.add(exam)
    await session.commit()
    await session.refresh(exam)
    stmt = select(Exam).options(joinedload(Exam.exam_type)).where(Exam.id== exam.id)
    res: Result = await session.execute(stmt)
    exam: Exam = res.scalar_one()
    return ExamCreated(
            id = exam.id,
            exam_name = exam.exam_type.name,
            exam_type_id = exam.exam_type_id,
            date = exam.date,
            next_date = exam.next_date,
            protocol=exam.protocol,
            notation=exam.notation,
            place=exam.place,
            employee_id=exam.employee_id
        )