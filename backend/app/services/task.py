# backend/app/services/task.py
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, TaskDetail
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.task_detail import TaskDetailCreate, TaskDetailUpdate


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks(
        self,
        user_id: int,
        is_completed: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Task], int]:
        query = select(Task).where(Task.user_id == user_id)
        if is_completed is not None:
            query = query.where(Task.is_completed == is_completed)
        query = query.order_by(Task.created_at.desc())

        # Count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Paginate
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await self.db.execute(query)
        tasks = list(result.scalars().all())

        return tasks, total

    async def get_task(self, task_id: int, user_id: int) -> Optional[Task]:
        result = await self.db.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
        task = Task(**task_data.model_dump(), user_id=user_id)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def update_task(self, task: Task, task_data: TaskUpdate) -> Task:
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()

    async def complete_task(self, task: Task) -> Task:
        task.is_completed = True
        task.complete_time = datetime.now()
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def defer_task(self, task: Task) -> tuple[Task, Task]:
        # Complete original task
        task.is_completed = True
        task.complete_time = datetime.now()

        # Create new task for tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

        new_task = Task(
            name=task.name,
            register_time=tomorrow_start,
            publisher=task.publisher,
            remark=task.remark,
            user_id=task.user_id,
            is_completed=False,
        )
        self.db.add(new_task)

        # Copy details
        result = await self.db.execute(
            select(TaskDetail).where(TaskDetail.task_id == task.id)
        )
        details = result.scalars().all()
        for detail in details:
            new_detail = TaskDetail(
                task_id=new_task.id,
                name=detail.name,
                progress=detail.progress,
                remark=detail.remark,
            )
            self.db.add(new_detail)

        await self.db.commit()
        await self.db.refresh(task)
        await self.db.refresh(new_task)
        return task, new_task

    # Task Details
    async def get_details(self, task_id: int) -> list[TaskDetail]:
        result = await self.db.execute(
            select(TaskDetail).where(TaskDetail.task_id == task_id).order_by(TaskDetail.created_at)
        )
        return list(result.scalars().all())

    async def create_detail(self, task_id: int, detail_data: TaskDetailCreate) -> TaskDetail:
        detail = TaskDetail(**detail_data.model_dump(), task_id=task_id)
        self.db.add(detail)
        await self.db.commit()
        await self.db.refresh(detail)
        return detail

    async def update_detail(self, detail: TaskDetail, detail_data: TaskDetailUpdate) -> TaskDetail:
        update_data = detail_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(detail, field, value)
        await self.db.commit()
        await self.db.refresh(detail)
        return detail

    async def delete_detail(self, detail: TaskDetail) -> None:
        await self.db.delete(detail)
        await self.db.commit()