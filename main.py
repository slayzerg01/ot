from fastapi import FastAPI, Depends, Request
from sqlalchemy import insert
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os

from core.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.api.schemas.employee import EmployeeSchema, EmployeeSchema_v2
from core.api.schemas.position import PositionSchema

from core.api.routers import employee
from core.api.routers import exam_types
from core.api.routers import divisions

from core.api.tools.position_tools import get_all_positions
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

folder = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=folder+"/static",html=True), name="static")
templates = Jinja2Templates(directory=folder+"/static/templates")

app.include_router(employee.router)
app.include_router(exam_types.router)
app.include_router(divisions.router)

@app.get("/")
async def root(request: Request, division: str | None = None, session: AsyncSession = Depends(get_async_session)):
    employees: list[EmployeeSchema_v2] = await employee.get_all_employees_v2(session=session, skip=0, limit=10, subdivision=division)
    positions: list[PositionSchema] = await get_all_positions(session=session)
    return templates.TemplateResponse("employees_list.html",
                                      {"request": request,
                                       "employees": employees,
                                       "positions": positions})

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
