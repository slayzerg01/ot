from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.exams import ExamResponse, ExamResponseWithEmployee, ExamCreate
from core.api.tools.exam_tools import get_all_exams_from_db, add_exam_in_db

router = APIRouter(
    prefix="/exams",
    tags=["exams"]
)

@router.get("/")
async def get_all_exams(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)) -> list[ExamResponseWithEmployee]: 
    return await get_all_exams_from_db(skip, limit, session)

@router.post("/add")
async def add_exam(employee_id: int, exam: ExamCreate, session: AsyncSession = Depends(get_async_session)):
    return await add_exam_in_db(employee_id=employee_id, new_exam=exam, session=session)
