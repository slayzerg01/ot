from sqlalchemy import Column, Integer, ForeignKey, DATE, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import BaseModel
from .employee import Employee

class Certificate(BaseModel):
    __tablename__ = 'certificates'

    number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    employee: Mapped[int] = mapped_column(Integer, ForeignKey(Employee.id), nullable=True)


class ExamType(BaseModel):
    __tablename__ = 'examtypes'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(500))
    period: Mapped[int] = mapped_column(Integer, nullable=False)


class Exam(BaseModel):
    __tablename__ = 'exams'

    date: Mapped[DATE] = mapped_column(DATE, nullable=False)
    next_date: Mapped[DATE] = mapped_column(DATE, nullable=False)
    protocol: Mapped[str] = mapped_column(String(255), nullable=False)
    employee: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey(Employee.id), 
        nullable= False)
    exam_type: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey(ExamType.id), 
        nullable= False)
    