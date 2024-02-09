from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.exams import ExamResponse, ExamResponseWithEmployee, ExamCreate, ExamUpdate
from core.api.tools.exam_tools import get_all_exams_from_db, add_exam_in_db, update_exam_in_db, del_exam_in_db
from core.models.User import User
from core.UserManager import current_active_verified_user

router = APIRouter(
    prefix="/exams",
    tags=["exams"]
)

@router.get("/")
async def get_all_exams(skip: int = 0, 
                        limit: int = 10, 
                        user: User = Depends(current_active_verified_user),
                        session: AsyncSession = Depends(get_async_session)
                        ) -> list[ExamResponseWithEmployee]: 
    return await get_all_exams_from_db(skip, limit, session)

@router.post("/add")
async def add_exam(employee_id: int, 
                   exam: ExamCreate, 
                   user: User = Depends(current_active_verified_user),
                   session: AsyncSession = Depends(get_async_session)):
    return await add_exam_in_db(employee_id=employee_id, new_exam=exam, session=session)

@router.patch("/update")
async def add_exam(exam_id: int, 
                   exam: ExamUpdate, 
                   user: User = Depends(current_active_verified_user),
                   session: AsyncSession = Depends(get_async_session)):
    return await update_exam_in_db(exam_id=exam_id, exam_update=exam, session=session)

@router.delete("/del")
async def add_exam(exam_id: int, 
                   user: User = Depends(current_active_verified_user),
                   session: AsyncSession = Depends(get_async_session)):
    return await del_exam_in_db(exam_id=exam_id, session=session)