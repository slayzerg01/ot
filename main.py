from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import os

from core.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.api.schemas.employee import EmployeeSchema_v2
from core.api.schemas.position import PositionSchema

from core.api.routers import employee
from core.api.routers import exam_types
from core.api.routers import divisions
from core.api.routers import subdivision

from core.api.tools.position_tools import get_all_positions
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
    cookie_max_age=3600,
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

current_user = fastapi_users.current_user()
current_active_verified_user = fastapi_users.current_user(active=True, verified=True, optional=True)


folder = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=folder+"/static/external/OT", html=True), name="static")
templates = Jinja2Templates(directory=folder+"/static/external/OT")

app.include_router(employee.router)
app.include_router(exam_types.router)
app.include_router(divisions.router)
app.include_router(subdivision.router)

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
    user: User | None = Depends(current_active_verified_user),
    session: AsyncSession = Depends(get_async_session)
):  
    if user is not None:
        employees: list[EmployeeSchema_v2] = await employee.get_all_employees_v2(session=session, skip=0, limit=10, subdivision=division)
        positions: list[PositionSchema] = await get_all_positions(session=session)
        return templates.TemplateResponse("index.html",
                                            {"request": request,
                                            "employees": employees,
                                            "positions": positions})
    else:
        return RedirectResponse(url="/login")


@app.get("/login")
async def root(request: Request):
    return templates.TemplateResponse("login.html",
                                      {"request": request})

# @app.exception_handler(HTTPException)
# async def http_exception(request: Request, exc: HTTPException):
#     if exc.status_code == 401:
#          return RedirectResponse(url="/login")
#     #return {"detail": exc.detail}
