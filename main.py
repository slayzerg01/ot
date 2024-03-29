from pathlib import Path
from fastapi import FastAPI, Depends, Header, Request, HTTPException, Response, status
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    RedirectResponse,
    StreamingResponse,
)
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os

from core.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.api.schemas.employee import EmployeeSchema_v2
from core.api.schemas.position import PositionRespone
from core.api.schemas.exam_types import ExamTypeResponse
from core.api.schemas.subdivision import SubdivisionResponse

from core.api.routers import employee
from core.api.routers import exam_types
from core.api.routers import divisions
from core.api.routers import subdivision
from core.api.routers import positions
from core.api.routers import exams
from core.api.routers import file

from core.api.tools.position_tools import get_all_positions_from_db
from core.api.tools.certificates_tool import get_all_certificates
from core.api.tools.exam_type_tools import get_all_exam_types_from_bd
from core.api.tools.division_tools import get_all_divisions_with_subdivision_from_db
from core.api.tools.subdivision_tools import get_all_subdivisions_from_db
from core.api.tools.exam_tools import get_all_exams_from_db, get_max_pages
from fastapi.middleware.cors import CORSMiddleware

from core.api.schemas.User import UserCreate, UserRead, UserUpdate
from core.models.User import User
from core.UserManager import (
    auth_backend,
    fastapi_users,
    current_user,
    current_active_verified_user,
)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


folder = os.path.dirname(__file__)
app.mount(
    "/static",
    StaticFiles(directory=folder + "/static/external/OT", html=True),
    name="static",
)
templates = Jinja2Templates(directory=folder + "/static/external/OT")

app.include_router(employee.router)
app.include_router(exam_types.router)
app.include_router(divisions.router)
app.include_router(subdivision.router)
app.include_router(positions.router)
app.include_router(exams.router)
app.include_router(file.router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
    tags=["users"],
)


@app.get("/")
async def root(
    request: Request,
    division: str | None = None,
    user: User | None = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user is not None:
        employees: list[
            EmployeeSchema_v2
        ] = await employee.get_all_employees_from_db_v2(
            session=session, skip=0, limit=10, subdivision=division
        )
        positions: list[PositionRespone] = await get_all_positions_from_db(
            session=session
        )
        examTypes: list[ExamTypeResponse] = await get_all_exam_types_from_bd(
            session=session
        )
        subdivisons: list[SubdivisionResponse] = await get_all_subdivisions_from_db(
            session=session,
            division_id=None
        )
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "employees": employees,
                "positions": positions,
                "examTypes": examTypes,
                "subdivisons": subdivisons,
            },
        )
    else:
        return RedirectResponse(url="/login")


@app.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/certificates")
async def get_certificate_page(
    request: Request,
    user: User = Depends(current_active_verified_user),
    assigned: bool | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    certificates = await get_all_certificates(session=session, assigned=assigned)
    return templates.TemplateResponse(
        "certificates.html",
        {"request": request, "certificates": certificates, "assigned": assigned},
    )


@app.get("/exam-types")
async def get_exam_types_page(
    request: Request,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    exam_types = await get_all_exam_types_from_bd(session)
    return templates.TemplateResponse(
        "exam-types.html", {"request": request, "exam_types": exam_types}
    )


@app.get("/positions")
async def get_positions_page(
    request: Request,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    positions = await get_all_positions_from_db(session)
    return templates.TemplateResponse(
        "positions.html", {"request": request, "positions": positions}
    )


@app.get("/divisions-page")
async def get_positions_page(
    request: Request,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    divisions = await get_all_divisions_with_subdivision_from_db(session)
    return templates.TemplateResponse(
        "divisions.html", {"request": request, "divisions": divisions}
    )


@app.get("/exams-list")
async def get_positions_page(
    request: Request,
    page: int = 1,
    user: User = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session),
):
    tmp = 20
    exams = await get_all_exams_from_db(
        skip=page * tmp - tmp, limit=tmp, session=session
    )
    max_page = await get_max_pages(skip=tmp, session=session)
    return templates.TemplateResponse(
        "exam-list.html",
        {"request": request, "exams": exams, "page": page, "max_page": max_page},
    )


files = {
    item: os.path.join("static/video", item) for item in os.listdir("static/video")
}


@app.get("/get_video/{video_name}")
async def video_endpoint(
    video_name: str,
    range: str = Header(None),
    user: User = Depends(current_active_verified_user),
):
    CHUNK_SIZE = 1024 * 1024
    video_path = Path(files.get(video_name))
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            "Content-Range": f"bytes {str(start)}-{str(end)}/{filesize}",
            "Accept-Ranges": "bytes",
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")


@app.get("/play_video/{video_name}")
async def play_video(
    video_name: str,
    request: Request,
    response_class=HTMLResponse,
    user: User = Depends(current_active_verified_user),
):
    video_path = files.get(video_name)
    if video_path:
        return templates.TemplateResponse(
            "video.html",
            {"request": request, "video": {"path": video_path, "name": video_name}},
        )
    else:
        return Response(status_code=404)


# @app.exception_handler(HTTPException)
# async def http_exception(request: Request, exc: HTTPException):
#     if exc.status_code == 401:
#          return RedirectResponse(url="/login")
#     #return {"detail": exc.detail}
