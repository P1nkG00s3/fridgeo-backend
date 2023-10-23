from pydantic.dataclasses import dataclass
from fastapi import APIRouter, HTTPException
from typing import List
@dataclass
class User:
    id: int
    username: str
    name: str
    age: int

users = [
    User(1, 'pink', 'Patric', 45),
    User(2, 'goose', 'John', 46),
]

user_router = APIRouter(prefix='/users', tags=['Пользователи'])

@user_router.get('/', name='Все пользователи', response_model=List[User])
def get_all_uses():
    return users


@user_router.post('/', name='Добавить пользователя', response_model=User)
def userAdd(user: User):
    users.append(user)
    return user


@user_router.get('/{user_id}', name='Получить пользователя', response_model=User)
def get_user(user_id: int):
    for user in users:
        if user_id == user.id:
            return user
    raise HTTPException(status_code=404, detail='User not found')
