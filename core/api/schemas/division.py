from pydantic import BaseModel, ConfigDict
from .subdivision import SubdivisionBase


class DivisionBase(BaseModel):
    name: str 
    model_config = ConfigDict(from_attributes=True)

class DivisionResponse(DivisionBase):
    id: int

class DivisionWithSubdivisions(DivisionResponse):
    subdivisions: list[SubdivisionBase]

class DivisionCreate(DivisionBase):
    pass

class DivisionUpdate(DivisionBase):
    pass