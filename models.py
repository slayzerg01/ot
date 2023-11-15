from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, DATE

from core.database import BaseModel


class Subdivision(BaseModel):
    __tablename__ = 'subdivision'

    name = Column(VARCHAR(255), nullable=False, unique=True)


class Position(BaseModel):
    __tablename__ = 'position'

    name = Column(VARCHAR(255), nullable=False, unique=True)


class Employee(BaseModel):
    __tablename__ = 'employee'

    FIO = Column(VARCHAR(255), nullable=False)
    position = Column(Integer, ForeignKey(Position.id))
    subdivision = Column(Integer, ForeignKey(Subdivision.id))


class Certificate(BaseModel):
    __tablename__ = 'certificate'

    number = Column(Integer, nullable=False, unique=True)
    subdivision = Column(Integer, ForeignKey(Employee.id))


class ExamType(BaseModel):
    __tablename__ = 'examtype'

    name = Column(VARCHAR(255), nullable=False, unique=True)
    description = Column(VARCHAR(500))
    period = Column(Integer, nullable=False)


class Exam(BaseModel):
    __tablename__ = 'exam'

    date = Column(DATE, nullable=False)
    next_date = Column(DATE, nullable=False)
    protocol = Column(VARCHAR(255), nullable=False)
    exam_type = Column(Integer, ForeignKey(ExamType.id))
