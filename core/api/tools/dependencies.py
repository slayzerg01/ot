from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.models.employee import Employee
from core.api.tools.employee_tools import get_employee

async def employee_by_id(employee_id: Annotated[int, Path], session: AsyncSession = Depends(get_async_session)) -> Employee:
    employee = await get_employee(session, None, employee_id)
    if employee is not None:
        return employee
    raise HTTPException(status_code=404, detail="Employee not found")