from sqlalchemy import Column, Integer, ForeignKey, DATE, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import BaseModel
from .employee import Employee

class Certificate(BaseModel):
    __tablename__ = 'certificates'

    number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey(Employee.id, ondelete='CASCADE'), nullable=True)

    employee = relationship("Employee", back_populates="certificate", passive_deletes=True)


class ExamType(BaseModel):
    __tablename__ = 'examtypes'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(500))
    period: Mapped[int] = mapped_column(Integer, nullable=False)

    exam = relationship("Exam", back_populates="exam_type", passive_deletes=True)


class Exam(BaseModel):
    __tablename__ = 'exams'

    date: Mapped[DATE] = mapped_column(DATE, nullable=False)
    next_date: Mapped[DATE] = mapped_column(DATE, nullable=False)
    protocol: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey(Employee.id), 
        nullable= False)
    exam_type_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey(ExamType.id), 
        nullable= False)
    
    employee = relationship("Employee", back_populates="exam", passive_deletes=True)
    exam_type = relationship("ExamType", back_populates="exam", passive_deletes=True)