from typing import Union

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from admin.auth.auth_dao import AuthUserDB


AuthUserDBPydantic = pydantic_model_creator(
    AuthUserDB,
    exclude=('id',),
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str
