from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    fio: str
    position_id: int
    subdivision_id: int
    model_config = ConfigDict(from_attributes=True)

class EmployeeSchema(EmployeeBase):
    id: int
    position: str
    subdivision: str

class EmployeeUpdate(EmployeeBase):
    fio: str | None = None
    position_id: int | None = None
    subdivision_id: int | None = None
    is_active: bool

class CreateEmployee(EmployeeBase):
    is_active: bool
    pass