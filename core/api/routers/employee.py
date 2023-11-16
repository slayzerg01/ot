from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.models.employee import Employee
from core.api.schemas.employee import EmployeeSchema
from core.api.tools.employee_tools import get_all_employees, get_employee, add_employee, del_employee
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
    
@router.get("/del", summary="delete employee")
async def read_employees(name: str = None, id: int = None, session: AsyncSession = Depends(get_async_session)):
    db_employee = await get_employee(session, name, id)
    if not db_employee:
        raise HTTPException(status_code=400, detail="Employee not exist")
    await del_employee(session, id, name)
    return [{"detail": f"{db_employee.fio} was deleted"}]

@router.get("/get", summary="get employee")
async def read_employees(id: int = None, name: str = None, session: AsyncSession = Depends(get_async_session)) -> EmployeeSchema:
    employee = await get_employee(session, name, id)
    if employee is None:
        raise HTTPException(status_code=404, detail="User not found")
    return employee
