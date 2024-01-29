from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.database import get_async_session
from core.api.schemas.position import PositionRespone, CreatePosition
from core.api.tools.position_tools import get_all_positions_from_db, update_position_in_db, add_position_in_db
from core.models.employee import Position
from core.api.tools.dependencies import position_by_id

router = APIRouter(
    prefix="/position",
    tags=["positions"]
)

@router.get("/")
async def read_positions(session: AsyncSession = Depends(get_async_session)) -> list[PositionRespone]: 
    return await get_all_positions_from_db(session)

@router.get("/{position_id}")
async def get_position(position: Position = Depends(position_by_id), 
                            session: AsyncSession = Depends(get_async_session)) -> PositionRespone:
    return position

@router.patch("/update/{position_id}")
async def update_position(position_update: CreatePosition, 
                           position: Position = Depends(position_by_id), 
                           session: AsyncSession = Depends(get_async_session)):
    return await update_position_in_db(
        session=session,
        position=position,
        position_update=position_update
    )

@router.post("/add")
async def add_position(new_position: CreatePosition, session: AsyncSession = Depends(get_async_session)):
    position = await add_position_in_db(session=session, new_position=new_position)
    return position


# @router.post("/add", summary="add exam_type")
# async def add_exam_type(new_exam_type: ExamTypeCreate, session: AsyncSession = Depends(get_async_session)):
#     employee = await add_exam_type_in_bd(session=session, new_exam_type=new_exam_type)
#     return employee