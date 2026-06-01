# backend/app/services/auth.py
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def create_user(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            password_hash=get_password_hash(user_data.password),
            role=user_data.role,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    def create_token(self, user: User) -> str:
        return create_access_token({"sub": str(user.id), "username": user.username})