from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import BaseModel


class Subdivision(BaseModel):
    __tablename__ = 'subdivisions'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    employees = relationship("Employee", back_populates="subdivision", passive_deletes=True)


class Position(BaseModel):
    __tablename__ = 'positions'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    employees = relationship("Employee", back_populates="position", passive_deletes=True)
    


class Employee(BaseModel):
    __tablename__ = 'employees'

    FIO: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey(Position.id, ondelete='CASCADE'), nullable=False)
    subdivision_id: Mapped[int] = mapped_column(Integer, ForeignKey(Subdivision.id, ondelete='CASCADE'), nullable=False)

    position = relationship("Position", back_populates="employees", passive_deletes=True)
    subdivision = relationship("Subdivision", back_populates="employees", passive_deletes=True)
    certificate = relationship("Certificate", back_populates="employee", passive_deletes=True)
    exam = relationship("Exam", back_populates="employee", passive_deletes=True)
