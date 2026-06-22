# backend/app/schemas/work_order.py
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class WorkOrderPriority(str, Enum):
    normal = "normal"
    medium = "medium"
    urgent = "urgent"


class WorkOrderCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    register_time: datetime
    publisher: str = Field(..., max_length=50)
    remark: Optional[str] = None
    priority: WorkOrderPriority = WorkOrderPriority.normal


class WorkOrderUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    register_time: Optional[datetime] = None
    publisher: Optional[str] = Field(None, max_length=50)
    is_completed: Optional[bool] = None
    remark: Optional[str] = None
    priority: Optional[WorkOrderPriority] = None


class WorkOrderResponse(BaseModel):
    id: int
    name: str
    register_time: datetime
    complete_time: Optional[datetime]
    publisher: str
    is_completed: bool
    remark: Optional[str]
    user_id: int
    priority: WorkOrderPriority
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WorkOrderListResponse(BaseModel):
    items: list[WorkOrderResponse]
    total: int
    page: int
    page_size: int
    pages: int
