from fastapi import FastAPI, Depends, Request
from sqlalchemy import insert
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os

from core.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.api.schemas.employee import EmployeeSchema, EmployeeSchema_v2

from core.api.routers import employee
from core.api.routers import exam_types


app = FastAPI()

folder = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=folder+"/static",html=True), name="static")
templates = Jinja2Templates(directory=folder+"/static/templates")

app.include_router(employee.router)
app.include_router(exam_types.router)

@app.get("/")
async def root(request: Request, division: str | None = None, session: AsyncSession = Depends(get_async_session)):
    employees: list[EmployeeSchema_v2] = await employee.get_all_employees_v2(session=session, skip=0, limit=10, subdivision=division)
    # positions: list[]
    return templates.TemplateResponse("employees_list.html",
                                      {"request": request,
                                       "employees": employees})

@app.get("/subdivisions")
async def root(request: Request, session: AsyncSession = Depends(get_async_session)):
    # stmt = insert(Position).values(
    #         name="test"
    #     )
    # print(stmt)
    # await session.execute(stmt)
    # await session.commit()
    return templates.TemplateResponse("subdivisions-settings.html",
                                      {"request": request})

@app.get("/test")
async def root():
    return True
