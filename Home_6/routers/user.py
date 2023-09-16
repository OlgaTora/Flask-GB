from typing import List
from fastapi import APIRouter, HTTPException, Path
from db import database, users
from models import User, UserIn

router = APIRouter()


@router.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    result = await database.fetch_all(query)
    if not result:
        raise HTTPException(status_code=404, detail="Table 'users' is empty")
    return result


@router.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int = Path(..., ge=1)):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="User didn't found")
    return result


@router.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password)
    last_id = await database.execute(query)
    return {**user.model_dump(), "id": last_id}


@router.put("/users/{user_id}", response_model=User)
async def update_user(new_user: UserIn, user_id: int = Path(..., ge=1)):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="User didn't found")
    return {**new_user.model_dump(), "id": user_id}


@router.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(..., ge=1)):
    query = users.delete().where(users.c.id == user_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="User didn't found")
    return {'message': 'User deleted'}
