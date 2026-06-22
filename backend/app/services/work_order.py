# backend/app/services/work_order.py
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.work_order import WorkOrder, WorkOrderDetail, WorkOrderPriority
from app.schemas.work_order import WorkOrderCreate, WorkOrderUpdate
from app.schemas.work_order_detail import WorkOrderDetailCreate, WorkOrderDetailUpdate


class WorkOrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_work_orders(
        self,
        user_id: int,
        is_completed: bool | None = None,
        page: int = 1,
        page_size: int = 20,
        start_dt=None,
        end_dt=None,
        priority: str | None = None,
        name: str | None = None,
    ):
        conditions = [WorkOrder.user_id == user_id]

        if is_completed is not None:
            conditions.append(WorkOrder.is_completed == is_completed)

        if start_dt:
            conditions.append(WorkOrder.register_time >= start_dt)
        if end_dt:
            conditions.append(WorkOrder.register_time < end_dt)
        if priority:
            try:
                prio_enum = WorkOrderPriority(priority)
                conditions.append(WorkOrder.priority == prio_enum)
            except ValueError:
                pass
        if name:
            conditions.append(WorkOrder.name.like(f"%{name}%"))

        # Count total
        count_query = select(func.count()).select_from(WorkOrder).where(and_(*conditions))
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Get paginated results
        offset = (page - 1) * page_size
        query = (
            select(WorkOrder)
            .where(and_(*conditions))
            .order_by(WorkOrder.register_time.desc())
            .offset(offset)
            .limit(page_size)
        )
        result = await self.db.execute(query)
        work_orders = result.scalars().all()

        return work_orders, total

    async def get_work_order(self, work_order_id: int, user_id: int):
        query = select(WorkOrder).where(
            and_(WorkOrder.id == work_order_id, WorkOrder.user_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_work_order(self, work_order_data: WorkOrderCreate, user_id: int):
        work_order = WorkOrder(
            name=work_order_data.name,
            register_time=work_order_data.register_time,
            publisher=work_order_data.publisher,
            remark=work_order_data.remark,
            priority=work_order_data.priority,
            user_id=user_id,
        )
        self.db.add(work_order)
        await self.db.commit()
        await self.db.refresh(work_order)
        return work_order

    async def update_work_order(self, work_order: WorkOrder, work_order_data: WorkOrderUpdate):
        update_data = work_order_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(work_order, field, value)
        await self.db.commit()
        await self.db.refresh(work_order)
        return work_order

    async def delete_work_order(self, work_order: WorkOrder):
        await self.db.delete(work_order)
        await self.db.commit()

    async def complete_work_order(self, work_order: WorkOrder):
        work_order.is_completed = True
        work_order.complete_time = datetime.now()
        await self.db.commit()
        await self.db.refresh(work_order)
        return work_order

    async def defer_work_order(self, work_order: WorkOrder):
        # Mark original as completed
        work_order.is_completed = True
        work_order.complete_time = datetime.now()

        # Create new work order for tomorrow
        tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        new_work_order = WorkOrder(
            name=work_order.name,
            register_time=tomorrow,
            publisher=work_order.publisher,
            remark=work_order.remark,
            priority=work_order.priority,
            user_id=work_order.user_id,
        )
        self.db.add(new_work_order)

        # Copy details to new work order
        details_query = select(WorkOrderDetail).where(WorkOrderDetail.work_order_id == work_order.id)
        details_result = await self.db.execute(details_query)
        original_details = details_result.scalars().all()

        for detail in original_details:
            new_detail = WorkOrderDetail(
                work_order_id=new_work_order.id,
                name=detail.name,
                progress=detail.progress,
                time=None,
                remark=detail.remark,
            )
            self.db.add(new_detail)

        await self.db.commit()
        await self.db.refresh(new_work_order)
        return work_order, new_work_order

    async def get_details(self, work_order_id: int):
        query = select(WorkOrderDetail).where(WorkOrderDetail.work_order_id == work_order_id).order_by(WorkOrderDetail.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_detail(self, work_order_id: int, detail_data: WorkOrderDetailCreate):
        detail = WorkOrderDetail(
            work_order_id=work_order_id,
            name=detail_data.name,
            progress=detail_data.progress,
            time=detail_data.time,
            remark=detail_data.remark,
        )
        self.db.add(detail)
        await self.db.commit()
        await self.db.refresh(detail)
        return detail

    async def update_detail(self, detail: WorkOrderDetail, detail_data: WorkOrderDetailUpdate):
        update_data = detail_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(detail, field, value)
        await self.db.commit()
        await self.db.refresh(detail)
        return detail

    async def delete_detail(self, detail: WorkOrderDetail):
        await self.db.delete(detail)
        await self.db.commit()
