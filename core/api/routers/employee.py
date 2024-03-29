from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.models.employee import Employee
from core.api.schemas.employee import (
    EmployeeSchema,
    EmployeeUpdate,
    EmployeeBase,
    CreateEmployee,
    EmployeeSchemWithExams,
)
from core.api.tools.employee_tools import (
    get_all_employees_from_db,
    get_employee_from_db,
    add_employee_in_db,
    del_employee_from_db,
    update_employee_in_db,
    get_all_employees_from_db_v2,
    get_all_employees_with_exams_from_db,
)
from core.api.tools.dependencies import employee_by_id
from sqlalchemy.exc import IntegrityError
from core.models.User import User
from core.UserManager import current_active_verified_user


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/get_all_with_exams", summary="get all employees with exams")
async def read_employees_with_exams(
    division: int = None,
    query: str = None,
    skip: int = 0,
    limit: int = 100,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[EmployeeSchemWithExams]:
    """
    Get list of employees with exams.
    - **division**: filtering employees by division
    - **query**: filtering employees by FIO
    - **skip**: offset of the array
    - **limit**: max count employees in result array
    """
    return await get_all_employees_with_exams_from_db(
        session=session, skip=skip, limit=limit, division=division, query=query
    )


@router.get("/", summary="get all employees")
async def read_employees(
    subdivision: str = None,
    skip: int = 0,
    limit: int = 100,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[EmployeeSchema]:
    """
    Get list of employees.
    - **subdivision**: filtering employees by division
    - **skip**: offset of the array
    - **limit**: max count employees in result array
    """
    return await get_all_employees_from_db(session, skip, limit, subdivision)


@router.post("/add", summary="add employee")
async def add_employee(
    new_employee: CreateEmployee,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create an employee with all the information:
    - **name**: each employee must have a name
    - **subdivision**: subdivision id
    - **position**: position id
    - **certificate**: certificate number
    """
    if await get_employee_from_db(session=session, name=new_employee.fio, id=None):
        raise HTTPException(status_code=404, detail="Employee already exist")
    else:
        try:
            employee = await add_employee_in_db(
                session=session, new_employee=new_employee
            )
            return employee
        except IntegrityError as ex:
            raise HTTPException(status_code=400, detail=str(ex))


@router.delete("/del/{employee_id}", summary="delete employee")
async def del_employee(
    employee: Employee = Depends(employee_by_id),
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Delete employee:
    - **employee_id**: employee id
    """
    await del_employee_from_db(employee, session)
    return [{"detail": f"{employee.fio} was deleted"}]


@router.get("/get/{employee_id}/", summary="get employee")
async def get_employees(
    employee: Employee = Depends(employee_by_id),
    user: User = Depends(current_active_verified_user),
) -> EmployeeSchema:
    """
    Get employee:
    - **employee_id**: employee id
    """
    return employee


@router.patch("/update/{employee_id}/", summary="update employee")
async def update_employee(
    employee_update: EmployeeUpdate,
    employee: Employee = Depends(employee_by_id),
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update employee:
    - **employee_id**: employee id
    - **name**: each employee must have a name
    - **subdivision**: subdivision id
    - **position**: position id
    - **certificate**: certificate number
    """
    return await update_employee_in_db(
        session=session, employee=employee, employee_update=employee_update
    )
