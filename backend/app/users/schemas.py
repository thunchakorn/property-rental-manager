from typing import Literal
from pydantic import Field, EmailStr

from ..schemas import BaseModel


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"] = "Bearer"


class RefreshRequest(BaseModel):
    grant_type: Literal["refresh_token"] | None = "refresh_token"
    refresh_token: str


class UserCreate(UserBase):
    password: str = Field(min_length=4)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john.doe@mail.com",
                    "password": "1234",
                    "first_name": "john",
                    "last_name": "doe",
                }
            ]
        }
    }


class UserPublic(UserBase):
    id: int
