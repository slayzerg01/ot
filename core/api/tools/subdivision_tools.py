from fastapi import HTTPException
from sqlalchemy import and_, select, or_, delete, update
from sqlalchemy.orm import joinedload
from core.models.employee import Subdivision
from sqlalchemy.engine import Result
from core.api.schemas.subdivision import SubdivisionResponse, UpdateSubdivision, SubdivisionBase
from sqlalchemy.ext.asyncio import AsyncSession
import sys
 


async def get_all_subdivisions_from_db(session: AsyncSession) -> list[SubdivisionResponse]:
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

async def update_subdivision(new_subdivision: Subdivision, session: AsyncSession):
    stmt = update(Subdivision).where(Subdivision.id == new_subdivision.id).values(name=new_subdivision.name, 
                                                                                  division_id=new_subdivision.division_id)
    await session.execute(stmt)
    await session.commit()

async def add_subdivision(new_subdivision: Subdivision, division_id: int, session: AsyncSession):
    subdivision = Subdivision()
    subdivision.name = new_subdivision.name
    subdivision.division_id = division_id
    session.add(subdivision)
    await session.commit()
    await session.refresh(subdivision)

async def update_and_add_subdivisions_in_db(subdivisions: UpdateSubdivision, session: AsyncSession):
    try:
        division_id = subdivisions.division_id

        for item in subdivisions.subdivisions.items():
            subdivision: Subdivision = Subdivision(
                name=item[1],
                id=int(item[0]),
                division_id=int(division_id)
            )
            if subdivision.id != 0:
                await update_subdivision(subdivision, session)
            else:
                await add_subdivision(subdivision, division_id, session)
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))

async def delete_subdivision_from_db(subdivision_id: int, session: AsyncSession):
    try:
        stmt = delete(Subdivision).where(Subdivision.id == subdivision_id)
        await session.execute(stmt)
        await session.commit()
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))
    
async def get_subdivision_by_id_from_db(subdivision_id: int, session: AsyncSession):
    try:
        stmt = select(Subdivision).options(joinedload(Subdivision.division)).where(Subdivision.id == subdivision_id)
        res: Result = await session.execute(stmt)
        return res.scalars().one_or_none()
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))
    