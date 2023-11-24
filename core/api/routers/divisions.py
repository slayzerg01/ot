from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.division import DivisionResponse
from core.api.tools.division_tools import get_all_divisions

router = APIRouter(
    prefix="/divisions",
    tags=["divisions"]
)

@router.get("/", summary="get all divisions")
async def get_divisions(session: AsyncSession = Depends(get_async_session)) -> list[DivisionResponse]: 
    return await get_all_divisions(session)