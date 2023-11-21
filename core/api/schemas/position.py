from pydantic import BaseModel

class PositionSchema(BaseModel):
    id: int
    name: str
