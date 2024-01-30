from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.subdivision import SubdivisionResponse, SubdivisionBase, UpdateSubdivision
from core.api.tools.subdivision_tools import get_all_subdivisions_from_db, update_and_add_subdivisions_in_db, delete_subdivision_from_db

router = APIRouter(
    prefix="/subdivisions",
    tags=["subdivisions"]
)

@router.get("/", summary="get all subdivisions")
async def get_subdivisions(session: AsyncSession = Depends(get_async_session)) -> list[SubdivisionResponse]: 
    return await get_all_subdivisions_from_db(session)

@router.patch("/update_subdivisions")
async def update_subdivisions(update_subdivisions: UpdateSubdivision, 
                              session: AsyncSession = Depends(get_async_session)): 
    await update_and_add_subdivisions_in_db(update_subdivisions, session)

@router.delete("/del/{subdivision_id}")
async def del_subdivision_by_id(subdivision_id: int, session: AsyncSession = Depends(get_async_session)):
    print("del tipa", subdivision_id)
    await delete_subdivision_from_db(subdivision_id=subdivision_id, session=session)
    return {'details': 'succes'}
    