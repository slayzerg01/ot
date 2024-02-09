from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
    JWTStrategy,
)
from core.models.User import User, get_user_manager
from fastapi_users import FastAPIUsers
from core.config import SECRET
import uuid

cookie_transport = CookieTransport(
    cookie_max_age=3600 * 8,
    cookie_name="ot_auth_token",
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600 * 8)


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
