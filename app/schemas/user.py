# app/schemas/user.py
from pydantic import BaseModel, EmailStr 
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr]

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: int

    class Config:
        from_attributes = True


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
