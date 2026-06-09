# backend/app/schemas/task.py
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class TaskPriority(str, Enum):
    normal = "normal"
    medium = "medium"
    urgent = "urgent"


class TaskCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    register_time: datetime
    publisher: str = Field(..., max_length=50)
    remark: Optional[str] = None
    priority: TaskPriority = TaskPriority.normal


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    register_time: Optional[datetime] = None
    publisher: Optional[str] = Field(None, max_length=50)
    is_completed: Optional[bool] = None
    remark: Optional[str] = None
    priority: Optional[TaskPriority] = None


class TaskResponse(BaseModel):
    id: int
    name: str
    register_time: datetime
    complete_time: Optional[datetime]
    publisher: str
    is_completed: bool
    remark: Optional[str]
    user_id: int
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int