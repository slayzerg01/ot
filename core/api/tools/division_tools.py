from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.employee import Division, Subdivision
from sqlalchemy.engine import Result
from core.api.schemas.division import DivisionResponse, DivisionWithSubdivisions, DivisionUpdate, DivisionCreate
from sqlalchemy.ext.asyncio import AsyncSession
import sys


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

async def update_division_in_db(session: AsyncSession, division_id: int, division_update: DivisionUpdate):
    try:
        update_data = division_update.model_dump(exclude_unset=True)
        stmt = update(Division).where(Division.id == division_id).values(update_data)
        await session.execute(stmt)
        await session.commit()
        stmt = select(Division).where(Division.id == division_id)
        res: Result = await session.execute(stmt)
        division: Division = res.scalar_one_or_none()
        return division
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))
    
async def add_division_in_db(session: AsyncSession, new_division: DivisionCreate):
    try:
        division = Division()
        division.name = new_division.name
        session.add(division)
        await session.commit()
        await session.refresh(division)
        return division
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))

async def delete_division_from_db(division_id: int, session: AsyncSession):
    try:
        stmt = delete(Division).where(Division.id == division_id)
        await session.execute(stmt)
        await session.commit()
        return {"detail": "succes"}
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))