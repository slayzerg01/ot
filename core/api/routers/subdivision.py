from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.subdivision import SubdivisionResponse
from core.api.tools.subdivision_tools import get_all_subdivisions

router = APIRouter(
    prefix="/subdivisions",
    tags=["subdivisions"]
)

@router.get("/", summary="get all subdivisions")
async def get_subdivisions(session: AsyncSession = Depends(get_async_session)) -> list[SubdivisionResponse]: 
    return await get_all_subdivisions(session)