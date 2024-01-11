from sqlalchemy.ext.asyncio import AsyncSession
from core.api.schemas.exams import ExamResponse
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from core.models.exam import Exam
from sqlalchemy.engine import Result
from core.api.schemas.exams import ExamResponse
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