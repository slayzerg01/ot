from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.employee import Division, Subdivision
from sqlalchemy.engine import Result
from core.api.schemas.division import DivisionResponse, DivisionWithSubdivisions
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_divisions_from_db(session: AsyncSession) -> list[DivisionResponse]:
    stmt = select(Division).order_by(Division.name)
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

async def get_all_divisions_with_subdivision_from_db(session: AsyncSession) -> list[DivisionWithSubdivisions]:
    stmt = select(Division).order_by(Division.name)
    res: Result = await session.execute(stmt)
    divisions: list[Division] = res.scalars().all()
    result = []
    for item in divisions:
        division : Division = item
        stmt = select(Subdivision).order_by(Subdivision.name).where(Subdivision.division_id == division.id)
        res: Result = await session.execute(stmt)
        subdivisions: list[Subdivision] = res.scalars().all()
        res: DivisionWithSubdivisions = DivisionWithSubdivisions(
            name=division.name,
            id=division.id,
            subdivisions=subdivisions
        )
        result.append(res)
    return result