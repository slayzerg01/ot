from sqlalchemy import select, update, delete
from core.models.employee import Position
from sqlalchemy.engine import Result
from core.api.schemas.position import PositionRespone, UpdatePosition, CreatePosition
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import sys


async def get_all_positions_from_db(session: AsyncSession) -> list[PositionRespone]:
    stmt = select(Position)
    res: Result = await session.execute(stmt)
    positions: list[Position] = res.scalars().all()
    result = []
    for item in positions:
        position: Position = item
        res: PositionRespone = PositionRespone(id=position.id, name=position.name)
        result.append(res)
    return result


async def get_position_by_id_from_db(session: AsyncSession, id: int) -> PositionRespone:
    stmt = select(Position).where(Position.id == id)
    res: Result = await session.execute(stmt)
    position: Position = res.scalar_one_or_none()
    if position:
        res: PositionRespone = PositionRespone(
            name=position.name,
            id=position.id,
        )
        return res
    else:
        return None


async def update_position_in_db(
    session: AsyncSession, position: Position, position_update: UpdatePosition
):
    try:
        update_data = position_update.model_dump(exclude_unset=True)
        stmt = update(Position).where(Position.id == position.id).values(update_data)
        await session.execute(stmt)
        await session.commit()
        stmt = select(Position).where(Position.id == position.id)
        res: Result = await session.execute(stmt)
        position: Position = res.scalar_one_or_none()
        return position
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def add_position_in_db(session: AsyncSession, new_position: CreatePosition):
    position = Position()
    position.name = new_position.name
    session.add(position)
    await session.commit()
    await session.refresh(position)
    return position


async def delete_position_from_db(session: AsyncSession, position_id: CreatePosition):
    try:
        stmt = delete(Position).where(Position.id == position_id)
        await session.execute(stmt)
        await session.commit()
    except:
        type, value, traceback = sys.exc_info()
        raise HTTPException(status_code=400, detail=str(value))
