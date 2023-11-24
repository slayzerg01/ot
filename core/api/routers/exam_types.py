from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.exam_types import ExamTypeResponse
from core.api.tools.exam_type_tools import get_all_exam_types
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/exam_types",
    tags=["exam_types"]
)

@router.get("/", summary="get all exam types")
async def read_employees(session: AsyncSession = Depends(get_async_session)) -> list[ExamTypeResponse]: 
    return await get_all_exam_types(session)