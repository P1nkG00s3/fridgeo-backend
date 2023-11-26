from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import psycopg2
from fastapi_users import FastAPIUsers



from fastapi import FastAPI, Depends


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
    tags=["Авторизация/Регистрация"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Авторизация/Регистрация"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route", tags=['GET Auth'])
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.name}"


@app.get("/good-man", tags=['Хороший человек'])
def good_man():
    return 'Федя гей'


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


