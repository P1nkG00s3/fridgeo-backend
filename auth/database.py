from typing import AsyncGenerator, TYPE_CHECKING

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Column, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from config import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    surname: Mapped[str] = mapped_column(
        String, nullable=False
    )
    sex: Mapped[str] = mapped_column(
        String, nullable=False
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )


# class Product(Base):
#     __tablename__ = "list_of_products"
#     if TYPE_CHECKING:  # pragma: no cover
#         id: int
#         name: str
#         category: str
#         amount: int
#         user_id: int
#     else:
#         name: Mapped[str] = mapped_column(
#             String, nullable=False
#         )
#         category: Mapped[str] = mapped_column(
#             String, nullable=False
#         )
#         amount: Mapped[int] = mapped_column(
#             Integer, nullable=False
#         )
#         user_id: Mapped[int] = mapped_column(
#             Integer, nullable=False
#         )
#         id: Mapped[int] = mapped_column(
#             Integer, primary_key=True
#         )


engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
SessionLocal = sessionmaker(autoflush=False, bind=engine)