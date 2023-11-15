from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.models.employee import Employee
from sqlalchemy.engine import Result
from core.api.schemas.employee import EmployeeSchema
from sqlalchemy.ext.asyncio import AsyncSession

async def get_employees(session: AsyncSession, skip: int, limit: int) -> list[EmployeeSchema]:
    stmt = select(Employee).options(joinedload(Employee.subdivision), joinedload(Employee.position)).offset(skip).limit(limit)
    res: Result = await session.execute(stmt)
    employees: list[Employee] = res.scalars().all()
    result = []
    for item in employees:
        employee : Employee = item
        print(employee.subdivision.id)
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