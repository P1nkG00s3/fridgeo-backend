from fastapi_users import fastapi_users, FastAPIUsers
from pydantic.dataclasses import dataclass
from fastapi import APIRouter, HTTPException, FastAPI
from typing import List

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.shemas import UserRead, UserCreate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(title="Fridgeo")


app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Авторизация"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Авторизация"],
)