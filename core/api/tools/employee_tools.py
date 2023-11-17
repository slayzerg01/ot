from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.employee import Employee
from sqlalchemy.engine import Result
from core.api.schemas.employee import EmployeeSchema, EmployeeUpdate, CreateEmployee
from sqlalchemy.ext.asyncio import AsyncSession


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