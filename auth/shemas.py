import re
import uuid
from datetime import date
from typing import Optional

from fastapi_users import schemas
from pydantic import field_validator, BaseModel, validator


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    name: str
    surname: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True

class UserCreate(schemas.BaseUserCreate):
    email: str

    # Define a validator for the email field
    @validator("email")
    def check_email(cls, value):
        # use a regex to check that the email has a valid format
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email address")
        return value

    password: str

    @validator("password")
    def check_password(cls, value):
        # convert the password to a string if it is not already
        value = str(value)
        # check that the password has at least 8 characters, one uppercase letter, one lowercase letter, and one digit
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        if (" " in value) or ('"' in value) or ("'" in value):
            raise ValueError("Password contains invalid characters")
        return value

    sex: str
    name: str
    surname: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class UserUpdate(schemas.BaseUserUpdate):
    pass


class Product(BaseModel):
    name: str
    category: str
    amount: int
    start_date: date
    expiration_date: date

    @validator("start_date")
    def validate_start_date(cls, value):
        # Добавляем проверку на корректность введенной даты
        if value > date.today():
            raise ValueError("Дата изготовления продукта не может быть в будущем")
        return value

    @validator("expiration_date")
    def validate_expiration_date(cls, value):
        # Добавляем проверку на корректность введенной даты
        if value < date.today():
            raise ValueError("Дата истечения срока годности не может быть в прошлом")
        return value

    class Config:
        orm_mode = True