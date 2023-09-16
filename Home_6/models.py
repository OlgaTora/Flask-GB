from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)
    password: str = Field(max_length=128, min_length=3)


class ProductIn(BaseModel):
    product_name: str = Field(max_length=32)
    description: str = Field(max_length=256)
    price: float = Field(gt=0)


class Product(ProductIn):
    id: int


class Status(str, Enum):
    DELIVERED = 'delivered'
    PAID = 'paid'
    ON_ROAD = 'on road'
    CANCEL = 'cancelled'


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: date
    status: Status

    class Config:
        use_enum_values = True


class Order(OrderIn):
    id: int


class OrderOut(BaseModel):
    id: int
    product_name: str = Field(max_length=32)
    price: float = Field(gt=0)
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    order_date: date
    status: Status
