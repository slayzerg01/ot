from sqlalchemy import String, Integer, ForeignKey, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import BaseModel


class Division(BaseModel):
    __tablename__ = "divisions"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    subdivision = relationship(
        "Subdivision", back_populates="division", passive_deletes=True
    )


class Subdivision(BaseModel):
    __tablename__ = "subdivisions"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    division_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Division.id), nullable=False
    )  # , ondelete='CASCADE'

    employees = relationship(
        "Employee", back_populates="subdivision", passive_deletes=True
    )
    division = relationship(
        "Division", back_populates="subdivision", passive_deletes=True
    )


class Position(BaseModel):
    __tablename__ = "positions"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    employees = relationship(
        "Employee", back_populates="position", passive_deletes=True
    )


class Employee(BaseModel):
    __tablename__ = "employees"

    FIO: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, nullable=False)
    position_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Position.id), nullable=False
    )  # , ondelete='CASCADE'
    subdivision_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Subdivision.id), nullable=False
    )  # , ondelete='CASCADE'

    position = relationship(
        "Position", back_populates="employees", passive_deletes=True
    )
    subdivision = relationship(
        "Subdivision", back_populates="employees", passive_deletes=True
    )
    certificate = relationship(
        "Certificate", back_populates="employee", passive_deletes=True
    )
    exam = relationship("Exam", back_populates="employee", passive_deletes=True)
