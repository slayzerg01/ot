from pydantic import BaseModel, ConfigDict
from datetime import date as py_date

class ExamBase(BaseModel):
    exam_type_id: int
    date: py_date
    next_date: py_date
    protocol: str
    notation: str
    place: str
    model_config = ConfigDict(from_attributes=True)

class ExamResponse(ExamBase):
    id: int
    exam_name: str
    
class ExamResponseWithEmployee(ExamBase):
    id: int
    employee_id: int
    employee: str
    exam_name: str

class ExamCreate(ExamBase):
    next_date: str | None
    notation: str | None

class ExamUpdate(ExamBase):
    next_date: py_date | None
    notation: str | None

class ExamCreated(ExamResponse):
    pass