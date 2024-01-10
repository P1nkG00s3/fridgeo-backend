from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import psycopg2
from fastapi_users import FastAPIUsers
from sqlmodel import SQLModel


from fastapi import FastAPI, Depends
from typing import List

from fastapi_users import FastAPIUsers
from fastapi import APIRouter, HTTPException, FastAPI, Depends, Body, status
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from auth.database import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from auth.shemas import Product as SchemaProduct
from models.models import ListOfProducts, Base
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.shemas import UserRead, UserCreate
from auth.auth import JWTStrategy

from config import *

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.shemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(title="Fridgeo")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
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


@app.post('/products', tags=['Products'])
async def add_product(product: SchemaProduct, current_user: User = Depends((current_user))):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    db_product = ListOfProducts(
        name=product.name,
        category=product.category,
        amount=product.amount,
        date_of_manufacture=product.start_date,
        expiration_date=product.expiration_date,
        user_id=current_user.id
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine) as session:
        session.add(db_product)
        await session.commit()
    return db_product


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiam9lQHh5ei5jb20iLCJleHBpcmVzIjoxNzAxNTIxNjUxLjI1NzI3NTN9.8yCnB29-1Jy7oe85Cfo_doXrZvW3J6qk69zy2rsaAEc
# Метод GET для получения всех продуктов
@app.get("/products/", tags=['Products'])
async def get_user_products(current_user: User = Depends(current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    async with AsyncSession(engine) as session:
        products = await session.execute(select(ListOfProducts).where(ListOfProducts.user_id == current_user.id))
        products = products.scalars().all()

        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found for the user")

        return products


@app.delete("/products/{product_id}", tags=['Products'])
async def delete_product_by_id(product_id: int, current_user: User = Depends(current_user)):
    # Проверка аутентификации пользователя
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    async with AsyncSession(engine) as session:
        # Поиск продукта по id и проверка, что он принадлежит текущему пользователю
        product = await session.execute(
            select(ListOfProducts).where(ListOfProducts.id == product_id, ListOfProducts.user_id == current_user.id))
        product = product.scalar()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id {product_id} not found for the user")
        else:
            # Удаление продукта
            await session.delete(product)
            await session.commit()  # Важный шаг: сохранение изменений в базе данных

    return {"message": f"Product with id {product_id} deleted successfully"}


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


