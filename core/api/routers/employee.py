from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.models.employee import Employee
from core.api.schemas.employee import EmployeeSchema, EmployeeUpdate, EmployeeBase, CreateEmployee, EmployeeSchemWithExams
from core.api.tools.employee_tools import get_all_employees_from_bd, get_employee_from_bd, add_employee_in_bd, del_employee_from_bd, update_employee_in_bd, get_all_employees_from_bd_v2, get_all_employees_with_exams_from_db
from core.api.tools.dependencies import employee_by_id
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)

@router.get("/get_all_with_exams", summary="get all employees with exams")
async def read_employees_with_exams(division: int = None, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)) -> list[EmployeeSchemWithExams]: 
    return await get_all_employees_with_exams_from_db(session, skip, limit, division)

@router.get("/", summary="get all employees")
async def read_employees(subdivision: str = None, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)) -> list[EmployeeSchema]: 
    """
    Get list of employees.
    - **subdivision**: filtering employees by division
    - **skip**: offset of the array
    - **limit**: max count employees in result array
    """
    return await get_all_employees_from_bd(session, skip, limit, subdivision)

@router.post("/add", summary="add employee")
async def add_employee(new_employee: CreateEmployee, session: AsyncSession = Depends(get_async_session)):
    """
    Create an employee with all the information:
    - **name**: each employee must have a name
    - **subdivision**: subdivision id 
    - **position**: position id 
    """
    if await get_employee_from_bd(session=session, name=new_employee.fio, id=None):
        raise HTTPException(status_code=404, detail="Employee already exist")
    else:
        try:
            employee = await add_employee_in_bd(session=session, new_employee=new_employee)
            return employee
        except IntegrityError as ex:
            raise HTTPException(status_code=400, detail=str(ex))
    
@router.delete("/del/{employee_id}/", summary="delete employee")
async def del_employee(employee: Employee = Depends(employee_by_id), session: AsyncSession = Depends(get_async_session)):
    await del_employee_from_bd(employee, session)
    return [{"detail": f"{employee.fio} was deleted"}]

@router.get("/get/{employee_id}/", summary="get employee")
async def get_employees(employee: Employee = Depends(employee_by_id)) -> EmployeeSchema:
    return employee

@router.patch("/update/{employee_id}/", summary="update employee")
async def update_employee(employee_update: EmployeeUpdate, 
                          employee: Employee = Depends(employee_by_id), 
                          session: AsyncSession = Depends(get_async_session)):
    return await update_employee_in_bd(
        session = session,
        employee = employee,
        employee_update = employee_update
    )
