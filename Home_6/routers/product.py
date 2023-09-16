import math
from typing import List

from fastapi import APIRouter, HTTPException, Path
from db import products, database
from models import Product, ProductIn

router = APIRouter()


@router.get('/products/', response_model=List[Product])
async def read_products():
    query = products.select()
    result = await database.fetch_all(query)
    if not result:
        raise HTTPException(status_code=404, detail="Table 'products' is empty")
    return result


@router.get('/products/{product_id}', response_model=Product)
async def read_product(product_id: int = Path(..., ge=1)):
    query = products.select().where(products.c.id == product_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Product didn't found")
    return result


@router.post('/products/', response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(
        product_name=product.product_name,
        description=product.description,
        price=product.price)
    last_id = await database.execute(query)
    return {**product.model_dump(), "id": last_id}


@router.put('/products/{product_id}', response_model=Product)
async def update_product(new_product: ProductIn, product_id: int = Path(..., ge=1)):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Product didn't found")
    return {**new_product.model_dump(), "id": product_id}


@router.delete('/products/{product_id}')
async def delete_product(product_id: int = Path(..., ge=1)):
    query = products.delete().where(products.c.id == product_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Product didn't found")
    return {'message': 'Product deleted'}
