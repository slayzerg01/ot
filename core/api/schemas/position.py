from pydantic import BaseModel

class PositionBase(BaseModel):
    name: str

class PositionRespone(PositionBase):
    id: int

class CreatePosition(PositionBase):
    pass

class UpdatePosition(PositionBase):
    name: str | None = None
