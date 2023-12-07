from pydantic import BaseModel, ConfigDict


class ExamTypeBase(BaseModel):
    name: str 
    model_config = ConfigDict(from_attributes=True)

class ExamTypeResponse(ExamTypeBase):
    id: int
    description: str
    period: int

class ExamTypeUpdate(ExamTypeBase):
    description: str | None = None
    period: int | None = None
    name: str | None = None

class ExamTypeCreate(ExamTypeBase):
    description: str 
    period: int
