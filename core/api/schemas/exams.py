from pydantic import BaseModel, ConfigDict
from datetime import date as py_date

class ExamBase(BaseModel):
    id: int
    exam_name: str
    exam_type_id: int
    date: py_date
    next_date: py_date
    model_config = ConfigDict(from_attributes=True)

class ExamResponse(ExamBase):
    protocol: str
    notation: str
    place: str