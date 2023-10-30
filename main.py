from fastapi_users import FastAPIUsers


#Ошибка в user 'is_acrivate == null'from fastapi_users import fastapi_users, FastAPIUsers
from pydantic.dataclasses import dataclass
from fastapi import APIRouter, HTTPException, FastAPI, Depends
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

current_user = fastapi_users.current_user()

@app.get("/protected-route", tags=['GET Auth'])
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.name}"



