from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os

from core.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.api.schemas.employee import EmployeeSchema_v2
from core.api.schemas.position import PositionRespone
from core.api.schemas.exam_types import ExamTypeResponse

from core.api.routers import employee
from core.api.routers import exam_types
from core.api.routers import divisions
from core.api.routers import subdivision
from core.api.routers import positions
from core.api.routers import exams

from core.api.tools.position_tools import get_all_positions_from_bd
from core.api.tools.certificates_tool import get_all_certificates
from core.api.tools.exam_type_tools import get_all_exam_types_from_bd
from core.api.tools.division_tools import get_all_divisions_with_subdivision_from_db
from fastapi.middleware.cors import CORSMiddleware

from core.api.schemas.User import UserCreate, UserRead, UserUpdate
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy
from core.models.User import User, get_user_manager
from fastapi_users import FastAPIUsers
from core.config import SECRET
import uuid


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cookie_transport = CookieTransport(
    cookie_max_age=3600*8,
    cookie_name='ot_auth_token',
    )

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(optional=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)


folder = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=folder+"/static/external/OT", html=True), name="static")
templates = Jinja2Templates(directory=folder+"/static/external/OT")

app.include_router(employee.router)
app.include_router(exam_types.router)
app.include_router(divisions.router)
app.include_router(subdivision.router)
app.include_router(positions.router)
app.include_router(exams.router)

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
    session: AsyncSession = Depends(get_async_session)
):  
    if user is not None:
        employees: list[EmployeeSchema_v2] = await employee.get_all_employees_from_bd_v2(session=session, skip=0, limit=10, subdivision=division)
        positions: list[PositionRespone] = await get_all_positions_from_bd(session=session)
        examTypes: list[ExamTypeResponse] = await get_all_exam_types_from_bd(session=session)
        return templates.TemplateResponse("index.html",
                                            {"request": request,
                                            "employees": employees,
                                            "positions": positions,
                                            "examTypes": examTypes})
    else:
        return RedirectResponse(url="/login")


@app.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html",
                                      {"request": request})

@app.get("/certificates")
async def get_certificate_page(request: Request, 
               user: User = Depends(current_active_verified_user),
               assigned: bool | None = None,
               session: AsyncSession = Depends(get_async_session)):
    certificates = await get_all_certificates(session=session, assigned=assigned)
    return templates.TemplateResponse("certificates.html",
                                      {"request": request,
                                       "certificates": certificates,
                                       "assigned": assigned})

@app.get("/exam-types")
async def get_exam_types_page(request: Request, 
               user: User = Depends(current_active_verified_user),
               session: AsyncSession = Depends(get_async_session)):
    exam_types = await get_all_exam_types_from_bd(session)
    return templates.TemplateResponse("exam-types.html",
                                      {"request": request,
                                       "exam_types": exam_types})

@app.get("/positions")
async def get_positions_page(request: Request, 
               user: User = Depends(current_active_verified_user),
               session: AsyncSession = Depends(get_async_session)):
    positions = await get_all_positions_from_bd(session)
    return templates.TemplateResponse("positions.html",
                                      {"request": request,
                                       "positions": positions})

@app.get("/divisions-page")
async def get_positions_page(request: Request, 
               user: User = Depends(current_active_verified_user),
               session: AsyncSession = Depends(get_async_session)):
    divisions = await get_all_divisions_with_subdivision_from_db(session)
    return templates.TemplateResponse("divisions.html",
                                      {"request": request,
                                       "divisions": divisions})

# @app.exception_handler(HTTPException)
# async def http_exception(request: Request, exc: HTTPException):
#     if exc.status_code == 401:
#          return RedirectResponse(url="/login")
#     #return {"detail": exc.detail}
