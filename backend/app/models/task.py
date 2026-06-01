# backend/app/models/task.py
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Task(Base):
    __tablename__ = "sys_task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    register_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    complete_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    publisher: Mapped[str] = mapped_column(String(50), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_user.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="tasks")
    details: Mapped[list["TaskDetail"]] = relationship("TaskDetail", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task {self.name}>"


class TaskDetail(Base):
    __tablename__ = "sys_task_detail"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_task.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    progress: Mapped[str | None] = mapped_column(String(50), nullable=True)
    time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    task: Mapped["Task"] = relationship("Task", back_populates="details")

    def __repr__(self):
        return f"<TaskDetail {self.name}>"


# Import User for relationship
from app.models.user import User  # noqa: E402, F401