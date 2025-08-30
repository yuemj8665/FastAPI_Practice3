# User 생성을 위한 요청 스키마
from pydantic import BaseModel
from typing import Union

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    email: Union[str, None] = None

class Token(BaseModel):
    access_token: str
    token_type: str