# backend/app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.user


class UserLogin(BaseModel):
    username: str
    password: str


# Alias for consistency with frontend
LoginRequest = UserLogin


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponse(Token):
    user: UserResponse