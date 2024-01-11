from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from core.config import DB_HOST, DB_USER, DB_PORT, DB_NAME, DB_PASS
from core.models.employee import Employee
from core.models.exam import Exam
from faker.providers import DynamicProvider
from datetime import timedelta
import random

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
session = Session(bind=engine)

fake = Faker(['ru_RU'])

exam_place_provider = DynamicProvider(
     provider_name="place",
     elements=["ИВЦ", "ФКЦ"],
)
fake.add_provider(exam_place_provider)


for i in range(100):
    exam = Exam()
    exam.date = fake.date_between()
    exam.next_date = exam.date + timedelta(days=365)
    exam.protocol = fake.passport_number()
    exam.employee_id = random.randint(14,65)
    exam.exam_type_id = random.randint(1,9)
    exam.notation = fake.text()
    exam.place = fake.place()
    session.add(exam)
    session.commit()

# for i in range(50):
#     employee = Employee()
#     employee.FIO = fake.name()
#     employee.is_active = True
#     employee.position_id = random.randint(1,7)
#     employee.subdivision_id = random.randint(1,7)
#     session.add(employee)
#     session.commit()
