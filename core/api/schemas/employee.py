from pydantic import BaseModel, ConfigDict
from .exams import ExamResponse


class EmployeeBase(BaseModel):
    fio: str
    position_id: int
    subdivision_id: int
    model_config = ConfigDict(from_attributes=True)

class EmployeeSchema(EmployeeBase):
    id: int
    position: str
    subdivision: str
   

class EmployeeSchema_v2(EmployeeBase):
    id: int
    position: str
    subdivision: str
    division: str
    certificate: int | None

class EmployeeSchemWithExams(EmployeeSchema_v2):
    exams: list[ExamResponse]

class EmployeeUpdate(EmployeeBase):
    fio: str | None = None
    position_id: int | None = None
    subdivision_id: int | None = None
    is_active: bool | None = None

class CreateEmployee(EmployeeBase):
    is_active: bool
    pass