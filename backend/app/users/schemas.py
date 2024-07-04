from typing import Literal
from pydantic import Field, EmailStr

from ..schemas import BaseModel


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"


class UserCreate(UserBase):
    password: str = Field(min_length=4)


class UserPublic(UserBase):
    id: int
