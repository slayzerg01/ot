from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.models.employee import Employee
from core.models.exam import ExamType
from core.models.employee import Position
from core.api.tools.employee_tools import get_employee_from_bd
from core.api.tools.exam_type_tools import get_exam_type_from_bd
from core.api.tools.position_tools import get_position_from_bd

async def employee_by_id(employee_id: Annotated[int, Path], session: AsyncSession = Depends(get_async_session)) -> Employee:
    employee = await get_employee_from_bd(session, None, employee_id)
    if employee is not None:
        return employee
    raise HTTPException(status_code=404, detail="Employee not found")

async def exam_type_by_id(exam_type_id: Annotated[int, Path], session: AsyncSession = Depends(get_async_session)) -> ExamType:
    exam_type = await get_exam_type_from_bd(session, exam_type_id)
    if exam_type is not None:
        return exam_type
    raise HTTPException(status_code=404, detail="Exam_type not found")

async def position_by_id(position_id: Annotated[int, Path], session: AsyncSession = Depends(get_async_session)) -> Position:
    position = await get_position_from_bd(session, position_id)
    if position is not None:
        return position
    raise HTTPException(status_code=404, detail="Position not found")