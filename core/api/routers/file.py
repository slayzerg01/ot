from fastapi import APIRouter, Depends, HTTPException, UploadFile
from openpyxl import load_workbook
import io
from core.api.schemas.subdivision import SubdivisionBase, SubdivisionResponse
from core.api.schemas.position import PositionRespone
from core.api.tools.subdivision_tools import get_all_subdivisions_from_db, add_subdivision
from core.models.database import get_async_session
from core.api.tools.position_tools import get_all_positions_from_db, add_position_in_db
from core.api.tools.employee_tools import add_import_employee
from core.api.tools.division_tools import get_all_divisions_from_db
from sqlalchemy.ext.asyncio import AsyncSession
from core.api.tools.employee_tools import get_employee_from_db
from core.api.schemas.position import CreatePosition
from core.models.employee import Subdivision
import sys

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

class CustomException(Exception):
    def __init__(self, text) -> None:
        self.value = text
        super().__init__(self.value)

@router.post("/upload")
async def upload_file(file: UploadFile, session: AsyncSession = Depends(get_async_session)):
    try:
        contents = file.file.read()
        filename=io.BytesIO(contents)
        book = load_workbook(filename=filename)
        sheet = book.active
        i = 2
        employee_list = [] 
        while sheet[f'A{i}'].value:
            fio = sheet[f'A{i}'].value
            subdivision = sheet[f'B{i}'].value
            position = sheet[f'C{i}'].value
            employee_list.append(EmployeeInfo(fio=fio, position=position, subdivision=subdivision))
            i += 1
        if i == 2:
            raise CustomException("Excel файл пустой")
        subdivisions: list[SubdivisionBase] = await get_all_subdivisions_from_db(session=session)
        positions: list[PositionRespone] = await get_all_positions_from_db(session=session)
        for employee in employee_list:
            for sub in subdivisions:
                if employee.subdivision[0] == sub.name:
                    employee.subdivision[1] = sub.id
                    break
            for pos in positions:
                if employee.position[0] == pos.name:
                    employee.position[1] = pos.id
                    break
            if not employee.position[1]:
                new_position = await add_position_in_db(new_position=CreatePosition(name=employee.position[0]), session=session)
                positions.append(PositionRespone(name=new_position.name, id=new_position.id))
                employee.position[1] = new_position.id
            
                
            employee_tmp = await get_employee_from_db(session=session, name=employee.fio, id=None)
            if not employee_tmp:
                await add_import_employee(fio=employee.fio,
                                          position_id=employee.position[1],
                                          subdivision_id=employee.subdivision[1],
                                          session=session)
        return {"details": 'succes'}
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))
    
class EmployeeInfo:
    def __init__(self, fio: str, position: str, subdivision: str):
        self.fio = fio
        self.position = [position, None]
        self.subdivision = [subdivision, None]
