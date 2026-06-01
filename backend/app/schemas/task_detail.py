# backend/app/schemas/task_detail.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class TaskDetailCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    progress: Optional[str] = Field(None, max_length=50)
    time: Optional[datetime] = None
    remark: Optional[str] = None


class TaskDetailUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    progress: Optional[str] = Field(None, max_length=50)
    time: Optional[datetime] = None
    remark: Optional[str] = None


class TaskDetailResponse(BaseModel):
    id: int
    task_id: int
    name: str
    progress: Optional[str]
    time: Optional[datetime]
    remark: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}