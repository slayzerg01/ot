from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    id: int
    fio: str
    position: str
    position_id: int
    subdivision: str
    subdivision_id: int