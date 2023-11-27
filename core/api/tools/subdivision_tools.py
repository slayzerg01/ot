from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.employee import Subdivision
from sqlalchemy.engine import Result
from core.api.schemas.subdivision import SubdivisionResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_subdivisions(session: AsyncSession) -> list[SubdivisionResponse]:
    stmt = select(Subdivision).order_by(Subdivision.name).options(joinedload(Subdivision.division))
    res: Result = await session.execute(stmt)
    subdivisions: list[Subdivision] = res.scalars().all()
    result = []
    for item in subdivisions:
        subdivision : Subdivision = item
        res: SubdivisionResponse = SubdivisionResponse(
            name=subdivision.name,
            id=subdivision.id,
            division=subdivision.division.name,
            division_id=subdivision.division_id
        )
        result.append(res)
    return result