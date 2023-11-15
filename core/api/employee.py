from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.database import get_async_session
from core.models.employee import Employee
from core.api.schemas.employee import EmployeeSchema
from core.api.tools.employee_tools import get_employees
from sqlalchemy.orm import joinedload
from sqlalchemy.engine import Result

router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)

@router.get("/get")
async def read_employees(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)) -> list[EmployeeSchema]: 
    return await get_employees(session, skip, limit)

@router.get("/add")
async def read_employees(s: int = None):
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/del")
async def read_employees():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/")
async def read_employees():
    return [{"username": "Rick"}, {"username": "Morty"}]
