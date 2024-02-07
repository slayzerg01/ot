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
from core.CustomExceptions import CustomException
import datetime


async def get_all_employees_from_db(session: AsyncSession, skip: int, limit: int, subdivision: str | None) -> list[EmployeeSchema]:
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

async def get_all_employees_from_db_v2(session: AsyncSession, skip: int, limit: int, subdivision: str | None) -> list[EmployeeSchema_v2]:
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

async def get_all_employees_with_exams_from_db(session: AsyncSession, skip: int, limit: int, division: int | None) -> list[EmployeeSchemWithExams]:
    stmt = select(Employee).options(joinedload(Employee.subdivision), joinedload(Employee.position)).where(Employee.is_active == True).order_by(Employee.FIO).offset(skip).limit(limit)
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
        if div.id == division or division == None:
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
    result.sort(key=lambda x: x.exams[0].next_date - datetime.date.today() if x.exams else datetime.timedelta(days=100000), reverse=False)        
    return result

async def get_employee_from_db(session: AsyncSession, name: str | None, id: int | None) -> EmployeeSchema:
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


async def add_employee_in_db(session: AsyncSession, new_employee: CreateEmployee):
    stmt = select(Certificate).where(Certificate.number == new_employee.certificate)
    res = await session.execute(stmt)
    certificate = res.scalar_one_or_none()
    if certificate.employee_id:
        return {'code': 1,
                'detail':'номер удостоверения уже используется, выберите другое значение'}
    else:
        employee = Employee()
        employee.FIO = new_employee.fio
        employee.subdivision_id = new_employee.subdivision_id
        employee.position_id = new_employee.position_id
        employee.is_active = True
        session.add(employee)
        await session.commit()
        await session.refresh(employee)
        stmt = update(Certificate).where(Certificate.number == new_employee.certificate).values(employee_id = employee.id)
        await session.execute(stmt)
        await session.commit()
        return employee


async def del_employee_from_db(employee: Employee, session: AsyncSession):
    stmt = update(Certificate).where(Certificate.employee_id == employee.id).values(employee_id = None)
    await session.execute(stmt)
    stmt = delete(Employee).where(Employee.id == employee.id)
    await session.execute(stmt)
    await session.commit()
    
async def update_employee_in_db(session: AsyncSession, employee: Employee, employee_update: EmployeeUpdate) -> EmployeeSchema_v2:
    try:
        update_data = employee_update.model_dump(exclude_unset=True)
        if 'fio' in update_data:
            update_data['FIO'] = update_data.pop('fio')
        if employee_update.certificate_id is not None:
            update_data.pop('certificate_id')
            stmt = select(Certificate).where(Certificate.number == employee_update.certificate_id)
            certificate_res = await session.execute(stmt)
            res = certificate_res.scalar_one_or_none() 
            if res.employee_id:
                raise CustomException('Номер удостоверения занят') 
            else:
                stmt = update(Certificate).where(Certificate.employee_id == employee.id).values(employee_id = None)
                await session.execute(stmt)
                stmt = update(Certificate).where(Certificate.number == employee_update.certificate_id).values(employee_id = employee.id)
                await session.execute(stmt)
        id = employee.id
        stmt = update(Employee).where(Employee.id == employee.id).values(update_data)
        await session.execute(stmt)
        stmt = select(Employee).where(Employee.id == id).options(joinedload(Employee.position), joinedload(Employee.subdivision))
        res: Result = await session.execute(stmt)
        employee: Employee = res.scalar_one_or_none()
        stmt = select(Division).where(Division.id == employee.subdivision.division_id)
        res: Result = await session.execute(stmt)
        division: Division = res.scalar_one_or_none()
        await session.commit()   

        response: EmployeeSchema_v2 = EmployeeSchema_v2(
            fio=employee.FIO,
            position_id=employee.position_id,
            subdivision_id=employee.subdivision_id,
            id= employee.id,
            position=employee.position.name,
            subdivision=employee.subdivision.name,
            division=division.name,
            certificate=employee_update.certificate_id
        )

        return response
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

async def add_import_employee(fio: str, position_id: int, subdivision_id: int, session: AsyncSession):
    employee = Employee()
    employee.FIO = fio
    employee.subdivision_id = subdivision_id
    employee.position_id = position_id
    employee.is_active = True
    session.add(employee)
    await session.commit()