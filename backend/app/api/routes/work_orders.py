# backend/app/api/routes/work_orders.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.work_order import WorkOrderCreate, WorkOrderUpdate, WorkOrderResponse, WorkOrderListResponse
from app.schemas.work_order_detail import WorkOrderDetailCreate, WorkOrderDetailUpdate, WorkOrderDetailResponse
from app.services.work_order import WorkOrderService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


@router.get("", response_model=WorkOrderListResponse)
async def get_work_orders(
    is_completed: Optional[bool] = Query(None),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    priority: Optional[str] = Query(None, description="优先级筛选"),
    name: Optional[str] = Query(None, description="工单名称搜索"),
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

    service = WorkOrderService(db)
    work_orders, total = await service.get_work_orders(
        current_user.id, is_completed, page, page_size,
        start_dt, end_dt, priority, name
    )
    pages = (total + page_size - 1) // page_size if total > 0 else 1
    return WorkOrderListResponse(
        items=[WorkOrderResponse.model_validate(wo) for wo in work_orders],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
async def get_work_order(
    work_order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    return WorkOrderResponse.model_validate(work_order)


@router.post("", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_work_order(
    work_order_data: WorkOrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.create_work_order(work_order_data, current_user.id)
    return WorkOrderResponse.model_validate(work_order)


@router.put("/{work_order_id}", response_model=WorkOrderResponse)
async def update_work_order(
    work_order_id: int,
    work_order_data: WorkOrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    updated = await service.update_work_order(work_order, work_order_data)
    return WorkOrderResponse.model_validate(updated)


@router.delete("/{work_order_id}")
async def delete_work_order(
    work_order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    await service.delete_work_order(work_order)
    return {"message": "WorkOrder deleted"}


@router.post("/{work_order_id}/complete", response_model=WorkOrderResponse)
async def complete_work_order(
    work_order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    completed = await service.complete_work_order(work_order)
    return WorkOrderResponse.model_validate(completed)


@router.post("/{work_order_id}/defer")
async def defer_work_order(
    work_order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    original, deferred = await service.defer_work_order(work_order)
    return {
        "original": WorkOrderResponse.model_validate(original),
        "deferred": WorkOrderResponse.model_validate(deferred),
    }


# WorkOrder Details
@router.get("/{work_order_id}/details", response_model=list[WorkOrderDetailResponse])
async def get_details(
    work_order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    details = await service.get_details(work_order_id)
    return [WorkOrderDetailResponse.model_validate(d) for d in details]


@router.post("/{work_order_id}/details", response_model=WorkOrderDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_detail(
    work_order_id: int,
    detail_data: WorkOrderDetailCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    detail = await service.create_detail(work_order_id, detail_data)
    return WorkOrderDetailResponse.model_validate(detail)


@router.put("/{work_order_id}/details/{detail_id}", response_model=WorkOrderDetailResponse)
async def update_detail(
    work_order_id: int,
    detail_id: int,
    detail_data: WorkOrderDetailUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    details = await service.get_details(work_order_id)
    detail = next((d for d in details if d.id == detail_id), None)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrderDetail not found")
    updated = await service.update_detail(detail, detail_data)
    return WorkOrderDetailResponse.model_validate(updated)


@router.delete("/{work_order_id}/details/{detail_id}")
async def delete_detail(
    work_order_id: int,
    detail_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = WorkOrderService(db)
    work_order = await service.get_work_order(work_order_id, current_user.id)
    if not work_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrder not found")
    details = await service.get_details(work_order_id)
    detail = next((d for d in details if d.id == detail_id), None)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="WorkOrderDetail not found")
    await service.delete_detail(detail)
    return {"message": "WorkOrderDetail deleted"}
