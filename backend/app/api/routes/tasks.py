# backend/app/api/routes/tasks.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.schemas.task_detail import TaskDetailCreate, TaskDetailUpdate, TaskDetailResponse
from app.services.task import TaskService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def get_tasks(
    is_completed: Optional[bool] = Query(None),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    priority: Optional[str] = Query(None, description="优先级筛选"),
    name: Optional[str] = Query(None, description="任务名称搜索"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 转换日期字符串
    start_dt = None
    end_dt = None
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid start_date format. Use YYYY-MM-DD")
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid end_date format. Use YYYY-MM-DD")

    task_service = TaskService(db)
    tasks, total = await task_service.get_tasks(
        current_user.id, is_completed, page, page_size,
        start_dt, end_dt, priority, name
    )
    pages = (total + page_size - 1) // page_size if total > 0 else 1
    return TaskListResponse(
        items=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse.model_validate(task)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.create_task(task_data, current_user.id)
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated = await task_service.update_task(task, task_data)
    return TaskResponse.model_validate(updated)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await task_service.delete_task(task)
    return {"message": "Task deleted"}


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    completed = await task_service.complete_task(task)
    return TaskResponse.model_validate(completed)


@router.post("/{task_id}/defer")
async def defer_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    original, deferred = await task_service.defer_task(task)
    return {
        "original": TaskResponse.model_validate(original),
        "deferred": TaskResponse.model_validate(deferred),
    }


# Task Details
@router.get("/{task_id}/details", response_model=list[TaskDetailResponse])
async def get_details(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    details = await task_service.get_details(task_id)
    return [TaskDetailResponse.model_validate(d) for d in details]


@router.post("/{task_id}/details", response_model=TaskDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_detail(
    task_id: int,
    detail_data: TaskDetailCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    detail = await task_service.create_detail(task_id, detail_data)
    return TaskDetailResponse.model_validate(detail)


@router.put("/{task_id}/details/{detail_id}", response_model=TaskDetailResponse)
async def update_detail(
    task_id: int,
    detail_id: int,
    detail_data: TaskDetailUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    details = await task_service.get_details(task_id)
    detail = next((d for d in details if d.id == detail_id), None)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TaskDetail not found")
    updated = await task_service.update_detail(detail, detail_data)
    return TaskDetailResponse.model_validate(updated)


@router.delete("/{task_id}/details/{detail_id}")
async def delete_detail(
    task_id: int,
    detail_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    details = await task_service.get_details(task_id)
    detail = next((d for d in details if d.id == detail_id), None)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TaskDetail not found")
    await task_service.delete_detail(detail)
    return {"message": "TaskDetail deleted"}