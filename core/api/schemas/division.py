from pydantic import BaseModel, ConfigDict


class DivisionBase(BaseModel):
    name: str 
    model_config = ConfigDict(from_attributes=True)

class DivisionResponse(DivisionBase):
    id: int
