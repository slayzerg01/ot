from sqlalchemy import and_, select, or_, delete
from sqlalchemy.orm import joinedload
from core.models.employee import Employee
from sqlalchemy.engine import Result
from core.api.schemas.employee import EmployeeSchema
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


async def add_employee(session, name: str, subdivision: int, position: int):
    employee = Employee()
    employee.FIO = name 
    employee.subdivision_id = subdivision
    employee.position_id =position
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    return employee


async def del_employee(session: AsyncSession, id: int | None , name: int | None):
    stmt = stmt = delete(Employee).where(or_(Employee.id == id, Employee.FIO == name))
    await session.execute(stmt)
    await session.commit()
    