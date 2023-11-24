from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.employee import Employee, Division
from core.models.exam import Certificate
from sqlalchemy.engine import Result
from core.api.schemas.employee import EmployeeSchema, EmployeeUpdate, CreateEmployee, EmployeeSchema_v2, EmployeeSchemWithExams
from core.api.schemas.exams import ExamResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.api.tools.exam_tools import get_all_exams_by_id
from typing import Any


async def get_all_employees(session: AsyncSession, skip: int, limit: int, subdivision: str | None) -> list[EmployeeSchema]:
    stmt = select(Employee).options(joinedload(Employee.subdivision), joinedload(Employee.position)).offset(skip).limit(limit)
    res: Result = await session.execute(stmt)
    employees: list[Employee] = res.scalars().all()
    result = []
    for item in employees:
        employee : Employee = item
        if employee.subdivision.name == subdivision or subdivision == None:
            res: EmployeeSchema = EmployeeSchema(
                fio=employee.FIO,
                id=employee.id,
                position=employee.position.name,
                position_id=employee.position.id,
                subdivision=employee.subdivision.name,
                subdivision_id=employee.subdivision.id
            )
            result.append(res)
    return result

async def get_all_employees_v2(session: AsyncSession, skip: int, limit: int, subdivision: str | None) -> list[EmployeeSchema_v2]:
    stmt = select(Employee).options(joinedload(Employee.subdivision), joinedload(Employee.position)).offset(skip).limit(limit)
    res: Result = await session.execute(stmt)
    employees: list[Employee] = res.scalars().all()
    result = []
    for item in employees:
        employee : Employee = item
        stmt = select(Division).where(Division.id == employee.subdivision.division_id)
        res: Result = await session.execute(stmt)
        div: Division = res.scalar_one_or_none()
        stmt = select(Certificate).where(Certificate.employee_id == employee.id)
        res: Result = await session.execute(stmt)
        cer: Certificate = res.scalar_one_or_none()
        if cer:
            cer = cer.number
        else:
            cer = None
        if employee.subdivision.name == subdivision or subdivision == None:
            res: EmployeeSchema_v2 = EmployeeSchema_v2(
                fio=employee.FIO,
                id=employee.id,
                position=employee.position.name,
                position_id=employee.position.id,
                subdivision=employee.subdivision.name,
                subdivision_id=employee.subdivision.id,
                division = div.name,
                division_id = div.id, 
                certificate = cer
            )
            result.append(res)
    return result

async def get_all_employees_with_exams(session: AsyncSession, skip: int, limit: int, subdivision: int | None) -> list[EmployeeSchemWithExams]:
    stmt = select(Employee).options(joinedload(Employee.subdivision), joinedload(Employee.position)).offset(skip).limit(limit)
    res: Result = await session.execute(stmt)
    employees: list[Employee] = res.scalars().all()
    result = []
    for item in employees:
        employee : Employee = item
        stmt = select(Division).where(Division.id == employee.subdivision.division_id)
        res: Result = await session.execute(stmt)
        div: Division = res.scalar_one_or_none()
        stmt = select(Certificate).where(Certificate.employee_id == employee.id)
        res: Result = await session.execute(stmt)
        cer: Certificate = res.scalar_one_or_none()
        if cer:
            certificate = cer.number
        else:
            certificate = None
        exams_by_id: list[ExamResponse] = await get_all_exams_by_id(session=session, skip=0, limit=10, id=employee.id)
        if employee.subdivision.id == subdivision or subdivision == None:
            res: EmployeeSchemWithExams = EmployeeSchemWithExams(
                fio=employee.FIO,
                id=employee.id,
                position=employee.position.name,
                position_id=employee.position.id,
                subdivision=employee.subdivision.name,
                subdivision_id=employee.subdivision.id,
                division = div.name,
                division_id = div.id, 
                certificate = certificate,
                exams = exams_by_id
            )
            result.append(res)
    return result

async def get_employee(session: AsyncSession, name: str | None, id: int | None) -> EmployeeSchema:
    stmt = select(Employee).options(joinedload(Employee.subdivision), joinedload(Employee.position)).where(or_(Employee.FIO == name, Employee.id == id))
    res: Result = await session.execute(stmt)
    employee: Employee = res.scalar_one_or_none()
    if employee :
        res: EmployeeSchema = EmployeeSchema(
            fio=employee.FIO,
            id=employee.id,
            position=employee.position.name,
            position_id=employee.position.id,
            subdivision=employee.subdivision.name,
            subdivision_id=employee.subdivision.id
        )
        return res
    else:
        return None


async def add_employee(session: AsyncSession, new_employee: CreateEmployee):
    employee = Employee()
    employee.FIO = new_employee.fio
    employee.subdivision_id = new_employee.subdivision_id
    employee.position_id = new_employee.position_id
    employee.is_active = new_employee.is_active
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


async def del_employee(employee: Employee, session: AsyncSession):
    stmt = delete(Employee).where(Employee.id == employee.id)
    await session.execute(stmt)
    await session.commit()
    
async def update_employee(session: AsyncSession, employee: Employee, employee_update: EmployeeUpdate):
    # for name, value in employee_update.model_dump(exclude_unset=True).items():
    #     setattr(employee, name, value)
    try:
        update_data = employee_update.model_dump(exclude_unset=True)
        update_data = employee_update.model_dump(exclude_unset=True)
        if 'fio' in update_data:
            update_data['FIO'] = update_data.pop('fio')
        id = employee.id
        stmt = update(Employee).where(Employee.id == employee.id).values(update_data)
        await session.execute(stmt)
        await session.commit()
        stmt = select(Employee).where(Employee.id == id)
        res: Result = await session.execute(stmt)
        employee: Employee = res.scalar_one_or_none()
        return employee
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))
