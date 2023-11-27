from pydantic import BaseModel, ConfigDict


class SubdivisionBase(BaseModel):
    id: int
    name: str 
    model_config = ConfigDict(from_attributes=True)

class SubdivisionResponse(SubdivisionBase):
    division_id: int
    division: str