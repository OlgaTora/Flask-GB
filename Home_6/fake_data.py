import datetime
import math
import random
from fastapi import APIRouter
from db import users, database, products, orders
from models import Status

router = APIRouter()

USER_COUNT = 10
PRODUCT_COUNT = 15
ORDERS_COUNT = 50


async def create_users(count: int):
    """Function for create fake users"""
    for i in range(count):
        query = users.insert().values(
            name=f'user{i}',
            surname=f'surname{i}',
            email=f'mail{i}@mail.ru',
            password=f'{str(i) * 8}')
        await database.execute(query)
    return {'message': f'{count} fake users create'}


async def create_products(count: int):
    """Function for create fake products"""
    for i in range(count):
        query = products.insert().values(
            product_name=f'product_{i}',
            description=f'this is a good product_{i}',
            price=f'{(i + 1) * math.pi ** 2}')
        await database.execute(query)
    return {'message': f'{count} fake products create'}


async def create_orders(count: int):
    """Function for create fake orders"""
    for i in range(count):
        query = orders.insert().values(
            user_id=random.randint(1, USER_COUNT),
            product_id=random.randint(1, PRODUCT_COUNT),
            order_date=datetime.date.today(),
            status=random.choice([Status.DELIVERED.value, Status.PAID.value, Status.CANCEL.value, Status.ON_ROAD.value]))
        await database.execute(query)
    return {'message': f'{count} fake orders create'}


@router.post('/fake_data/')
async def make_fake_data():
    await create_users(USER_COUNT)
    await create_products(PRODUCT_COUNT)
    await create_orders(ORDERS_COUNT)
