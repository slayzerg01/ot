from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.models.employee import Employee
from core.api.schemas.employee import EmployeeSchema, EmployeeUpdate, EmployeeBase
from core.api.tools.employee_tools import get_all_employees, get_employee, add_employee, del_employee, update_employee
from core.api.tools.dependencies import employee_by_id
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)

@router.get("/get_all", summary="get all employees")
async def read_employees(subdivision: str = None, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)) -> list[EmployeeSchema]: 
    """
    Get list of employees.
    - **subdivision**: filtering employees by division
    - **skip**: offset of the array
    - **limit**: max count employees in result array
    """
    return await get_all_employees(session, skip, limit, subdivision)

@router.post("/add", summary="add employee")
async def read_employees(name: str, subdivision: int, position: int, session: AsyncSession = Depends(get_async_session)):
    """
    Create an employee with all the information:
    - **name**: each employee must have a name
    - **subdivision**: subdivision id 
    - **position**: position id 
    """
    db_employee = await get_employee(session, name, None)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already exist")
    try:
        employee = await add_employee(session, name, subdivision, position)
        return employee
    except IntegrityError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    
@router.get("/del/{employee_id}/", summary="delete employee")
async def read_employees(employee: Employee = Depends(employee_by_id), session: AsyncSession = Depends(get_async_session)):
    await del_employee(employee, session)
    return [{"detail": f"{employee.fio} was deleted"}]

@router.get("/get/{employee_id}/", summary="get employee")
async def read_employees(employee: Employee = Depends(employee_by_id)) -> EmployeeSchema:
    return employee

@router.put("/update/{employee_id}/", summary="update employee")
async def update(employee_update: EmployeeUpdate, employee: Employee = Depends(employee_by_id), session: AsyncSession = Depends(get_async_session)):
    return await update_employee(
        session = session,
        employee = employee,
        employee_update = employee_update
    )
