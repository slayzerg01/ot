from pydantic import BaseModel, ConfigDict


class ExamTypeBase(BaseModel):
    name: str 
    model_config = ConfigDict(from_attributes=True)

class ExamTypeResponse(ExamTypeBase):
    id: int
    description: str
    period: int
