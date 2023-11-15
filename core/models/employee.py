from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import BaseModel


class Subdivision(BaseModel):
    __tablename__ = 'subdivisions'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    employees = relationship("Employee", back_populates="subdivision")


class Position(BaseModel):
    __tablename__ = 'positions'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    employees = relationship("Employee", back_populates="position")


class Employee(BaseModel):
    __tablename__ = 'employees'

    FIO: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey(Position.id), nullable=False)
    subdivision_id: Mapped[int] = mapped_column(Integer, ForeignKey(Subdivision.id), nullable=False)

    position = relationship("Position", back_populates="employees")
    subdivision = relationship("Subdivision", back_populates="subdivision")
