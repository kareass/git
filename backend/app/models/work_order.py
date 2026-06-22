# backend/app/models/work_order.py
import enum
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey, func, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class WorkOrderPriority(str, enum.Enum):
    normal = "normal"
    medium = "medium"
    urgent = "urgent"


class WorkOrder(Base):
    __tablename__ = "sys_work_order"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    register_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    complete_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    publisher: Mapped[str] = mapped_column(String(50), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[WorkOrderPriority] = mapped_column(
        SQLEnum(WorkOrderPriority), default=WorkOrderPriority.normal, nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_user.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="work_orders")
    details: Mapped[list["WorkOrderDetail"]] = relationship("WorkOrderDetail", back_populates="work_order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WorkOrder {self.name}>"


class WorkOrderDetail(Base):
    __tablename__ = "sys_work_order_detail"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    work_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_work_order.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    progress: Mapped[str | None] = mapped_column(String(50), nullable=True)
    time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    work_order: Mapped["WorkOrder"] = relationship("WorkOrder", back_populates="details")

    def __repr__(self):
        return f"<WorkOrderDetail {self.name}>"


# Import User for relationship
from app.models.user import User  # noqa: E402, F401
