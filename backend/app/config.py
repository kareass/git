# backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # 数据库
    DATABASE_URL: str = "mysql+aiomysql://root:root@localhost:3306/work_statistics"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:5174"]

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()