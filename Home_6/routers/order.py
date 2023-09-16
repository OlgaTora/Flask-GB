import datetime
import random
from typing import List

from fastapi import APIRouter, Path, HTTPException
from sqlalchemy import select

from db import orders, database, products, users
from models import Order, OrderIn, OrderOut

router = APIRouter()


@router.get('/orders/', response_model=List[OrderOut])
async def read_orders():
    query = select(orders.c.id, orders.c.order_date, orders.c.status,
                   products.c.product_name, products.c.price,
                   users.c.name, users.c.surname).join(products).join(users)
    result = await database.fetch_all(query)
    if not result:
        raise HTTPException(status_code=404, detail="Table 'orders' is empty")
    return result


@router.get('/orders/{order_id}', response_model=OrderOut)
async def read_order(order_id: int = Path(..., ge=1)):
    query = select(orders.c.id, orders.c.order_date, orders.c.status,
                   products.c.product_name, products.c.price,
                   users.c.name, users.c.surname).where(orders.c.id == order_id).join(products).join(users)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Order didn't found")
    return result


@router.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        order_date=order.order_date,
        status=order.status)
    last_id = await database.execute(query)
    return {**order.model_dump(), "id": last_id}


@router.put('/orders/{order_id}', response_model=Order)
async def update_order(new_order: OrderIn, order_id: int = Path(..., ge=1)):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Order didn't found")
    return {**new_order.model_dump(), "id": order_id}


@router.delete('/orders/{order_id}')
async def delete_order(order_id: int = Path(..., ge=1)):
    query = orders.delete().where(orders.c.id == order_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Order didn't found")
    return {'message': 'Order deleted'}

#
# @router.post('/fake_orders/{count}')
# async def create_note(count: int):
#     """Function for create fake db"""
#     for i in range(count):
#         query = orders.insert().values(
#             user_id=random.randint(1, 10),
#             product_id=random.randint(1, 25),
#             order_date=datetime.date.today(),
#             status=random.choice(['delivered', 'payed', 'on road']))
#         await database.execute(query)
#     return {'message': f'{count} fake orders create'}
