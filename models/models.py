from datetime import datetime
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable
from sqlalchemy import MetaData, JSON, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declarative_base
from pydantic import BaseModel, Field
from auth.database import engine

Base = declarative_base()

# def password_ver(password:str):
#     l, u, p, d = 0, 0, 0, 0
#     capitalalphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     smallalphabets = "abcdefghijklmnopqrstuvwxyz"
#     specialchar = """ ~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/ """
#     digits = "0123456789"
#     if (len(password) >= 8):
#         for i in password:
#
#     # counting lowercase alphabets
#     if (i in smallalphabets):
#         l += 1
#
#     # counting uppercase alphabets
#     if (i in capitalalphabets):
#         u += 1
#
#     # counting digits
#     if (i in digits):
#         d += 1
#
#     # counting the mentioned special characters
#     if (i in specialchar):
#         p += 1
#     if (l >= 1 and u >= 1 and p >= 1 and d >= 1 and l + p + u + d == len(s)):
#         return password



password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class Password(BaseModel):
    password: str = Field(..., regex=password_regex)

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
