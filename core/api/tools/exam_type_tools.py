from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.exam import ExamType
from sqlalchemy.engine import Result
from core.api.schemas.exam_types import ExamTypeResponse, ExamTypeUpdate, ExamTypeCreate
from sqlalchemy.ext.asyncio import AsyncSession
import sys


async def get_all_exam_types_from_bd(session: AsyncSession) -> list[ExamTypeResponse]:
    stmt = select(ExamType).order_by(ExamType.name)
    res: Result = await session.execute(stmt)
    exam_types: list[ExamType] = res.scalars().all()
    result = []
    for item in exam_types:
        exam_type : ExamType = item
        res: ExamTypeResponse= ExamTypeResponse(
            name=exam_type.name,
            id=exam_type.id,
            description=exam_type.description,
            period=exam_type.period
        )
        result.append(res)
    return result

async def get_exam_type_from_bd(session: AsyncSession, id: int) -> ExamTypeResponse:
    stmt = select(ExamType).where(ExamType.id == id)
    res: Result = await session.execute(stmt)
    exam_type: ExamType = res.scalar_one_or_none()
    if exam_type:
        res: ExamTypeResponse = ExamTypeResponse(
            name=exam_type.name,
            id=exam_type.id,
            period=exam_type.period,
            description=exam_type.description
        )
        return res
    else:
        return None

async def update_exam_type_in_bd(session: AsyncSession, exam_type: ExamType, exam_type_update: ExamTypeUpdate):
    try:
        update_data = exam_type_update.model_dump(exclude_unset=True)
        stmt = update(ExamType).where(ExamType.id == exam_type.id).values(update_data)
        await session.execute(stmt)
        await session.commit()
        stmt = select(ExamType).where(ExamType.id == exam_type.id)
        res: Result = await session.execute(stmt)
        exam_type: ExamType = res.scalar_one_or_none()
        return exam_type
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

async def add_exam_type_in_bd(session: AsyncSession, new_exam_type: ExamTypeCreate):
    try:
        exam_type = ExamType()
        exam_type.name = new_exam_type.name
        exam_type.period = new_exam_type.period
        exam_type.description = new_exam_type.description
        session.add(exam_type)
        await session.commit()
        await session.refresh(exam_type)
        return exam_type
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))

async def delete_exam_type_from_db(exam_type_id: int, session: AsyncSession):
    try:
        stmt = delete(ExamType).where(ExamType.id == exam_type_id)
        await session.execute(stmt)
        await session.commit()
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))