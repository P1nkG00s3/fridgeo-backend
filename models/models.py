import datetime
from datetime import date
from fastapi import Depends
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable
from sqlalchemy import MetaData, JSON, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean, DateTime,Date, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from pydantic import Field, BaseModel, EmailStr
from sqlmodel import Session

from auth.database import engine


# Base = declarative_base()
class Base(DeclarativeBase):
    pass


password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"



class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    sex: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class ListOfProducts(Base):
    __tablename__ = "List Of Products"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    category: Mapped[str] = Column(String, nullable=False)
    amount: Mapped[int] = Column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date_of_manufacture: Mapped[Date] = Column(Date)
    expiration_date: Mapped[Date] = Column(Date)
    # date_of_manufacture: Mapped[DateTime] = Column(DateTime)
    # expiration_date: Mapped[DateTime] = Column(DateTime, server_default=func.now())

# class UserSchema(BaseModel):
#     fullname: str = Field(...)
#     email: EmailStr = Field(...)
#     password: str = Field(...)
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "fullname": "Joe Doe",
#                 "email": "joe@xyz.com",
#                 "password": "any"
#             }
#         }
#
# class UserLoginSchema(BaseModel):
#     email: EmailStr = Field(...)
#     password: str = Field(...)
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "email": "joe@xyz.com",
#                 "password": "any"
#             }
#         }