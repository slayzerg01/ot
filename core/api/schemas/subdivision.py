from pydantic import BaseModel, ConfigDict
from typing import Dict


class SubdivisionBase(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class SubdivisionResponse(SubdivisionBase):
    division_id: int
    division: str


class UpdateSubdivision(BaseModel):
    division_id: int
    subdivisions: Dict[str, str]
