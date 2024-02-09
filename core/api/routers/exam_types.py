from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.exam_types import ExamTypeResponse, ExamTypeUpdate, ExamTypeCreate
from core.api.tools.exam_type_tools import (
    get_all_exam_types_from_bd,
    update_exam_type_in_bd,
    add_exam_type_in_bd,
    delete_exam_type_from_db,
)
from core.models.exam import ExamType
from core.api.tools.dependencies import exam_type_by_id
from core.models.User import User
from core.UserManager import current_active_verified_user

router = APIRouter(prefix="/exam_types", tags=["exam_types"])


@router.get("/", summary="get all exam types")
async def read_exam_types(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
) -> list[ExamTypeResponse]:
    return await get_all_exam_types_from_bd(session)


@router.patch("/update/{exam_type_id}")
async def update_exam_type(
    exam_type_update: ExamTypeUpdate,
    exam_type: ExamType = Depends(exam_type_by_id),
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await update_exam_type_in_bd(
        session=session, exam_type=exam_type, exam_type_update=exam_type_update
    )


@router.post("/add", summary="add exam_type")
async def add_exam_type(
    new_exam_type: ExamTypeCreate,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    employee = await add_exam_type_in_bd(session=session, new_exam_type=new_exam_type)
    return employee


@router.delete("/delete/{exam_type_id}")
async def delete_exam_type(
    exam_type_id: int,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    await delete_exam_type_from_db(exam_type_id=exam_type_id, session=session)
    return {"detail": "succes"}
