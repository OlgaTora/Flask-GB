from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    username: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)


class UserIn(BaseModel):
    username: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)
    password: str = Field(max_length=128, min_length=3)
