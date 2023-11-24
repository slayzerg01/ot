from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.employee import Division
from sqlalchemy.engine import Result
from core.api.schemas.division import DivisionResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_divisions(session: AsyncSession) -> list[DivisionResponse]:
    stmt = select(Division)
    res: Result = await session.execute(stmt)
    divisions: list[Division] = res.scalars().all()
    result = []
    for item in divisions:
        division : Division = item
        res: DivisionResponse = DivisionResponse(
            name=division.name,
            id=division.id,
        )
        result.append(res)
    return result