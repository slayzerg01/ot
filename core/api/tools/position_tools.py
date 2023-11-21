from sqlalchemy import select
from core.models.employee import Position
from sqlalchemy.engine import Result
from core.api.schemas.position import PositionSchema
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all_positions(session: AsyncSession) -> list[PositionSchema]:
    stmt = select(Position)
    res: Result = await session.execute(stmt)
    positions: list[Position] = res.scalars().all()
    result = []
    for item in positions:
        position : Position= item
        res: PositionSchema = PositionSchema(
            id=position.id,
            name= position.name
        )
        result.append(res)
    return result