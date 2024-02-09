from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.division import DivisionResponse, DivisionCreate, DivisionUpdate
from core.api.tools.division_tools import (
    get_all_divisions_from_db,
    update_division_in_db,
    add_division_in_db,
    delete_division_from_db,
)
from core.models.User import User
from core.UserManager import current_active_verified_user

router = APIRouter(prefix="/divisions", tags=["divisions"])


@router.get("/", summary="get all divisions")
async def get_divisions(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
) -> list[DivisionResponse]:
    return await get_all_divisions_from_db(session)


@router.patch("/update/{division_id}")
async def update_division(
    division_id: int,
    new_division: DivisionUpdate,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> DivisionResponse:
    return await update_division_in_db(
        session=session, division_id=division_id, division_update=new_division
    )


@router.post("/add")
async def add_division(
    new_division: DivisionCreate,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> DivisionResponse:
    return await add_division_in_db(session=session, new_division=new_division)


@router.delete("/delete/{division_id}")
async def del_division(
    division_id: int,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_division_from_db(session=session, division_id=division_id)
