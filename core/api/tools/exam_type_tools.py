from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.exam import ExamType
from sqlalchemy.engine import Result
from core.api.schemas.exam_types import ExamTypeResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_exam_types(session: AsyncSession, skip: int, limit: int) -> list[ExamTypeResponse]:
    stmt = select(ExamType).offset(skip).limit(limit)
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