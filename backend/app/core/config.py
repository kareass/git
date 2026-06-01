# backend/app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://root:password@localhost:3306/work_statistics"
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:5174"]

    class Config:
        env_file = ".env"
        extra = "allow"