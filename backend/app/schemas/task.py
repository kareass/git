# backend/app/schemas/task.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class TaskCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    register_time: datetime
    publisher: str = Field(..., max_length=50)
    remark: Optional[str] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    register_time: Optional[datetime] = None
    publisher: Optional[str] = Field(None, max_length=50)
    remark: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    name: str
    register_time: datetime
    complete_time: Optional[datetime]
    publisher: str
    is_completed: bool
    remark: Optional[str]
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int