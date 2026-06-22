# backend/app/models/user.py
from datetime import datetime
from sqlalchemy import String, Enum as SQLEnum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "sys_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.user, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")
    work_orders: Mapped[list["WorkOrder"]] = relationship("WorkOrder", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"