from fastapi import FastAPI, Depends, Request
from sqlalchemy import insert
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models import Position

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

@app.get("/")
async def root(request: Request, session: AsyncSession = Depends(get_async_session)):
    # stmt = insert(Position).values(
    #         name="test"
    #     )
    # print(stmt)
    # await session.execute(stmt)
    # await session.commit()
    return templates.TemplateResponse("index.html",
                                      {"request": request})



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
