# app/schemas/user.py
from pydantic import BaseModel, EmailStr , validator
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

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    token: str
    password: str
    confirm_password: str

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v