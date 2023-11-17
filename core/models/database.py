from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import DB_HOST, DB_USER, DB_PORT, DB_NAME, DB_PASS
from typing import AsyncGenerator
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func
from datetime import datetime

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL) # echo=True
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
