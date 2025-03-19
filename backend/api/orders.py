from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from backend.database import get_db
from backend.models.orders import Order
from backend.schemas.orders import OrderCreate, OrderUpdate

router = APIRouter()

@router.get("/orders", response_model=list[OrderCreate])
async def get_orders(db: AsyncSession = Depends(get_db)):
    """Retrieve all orders."""
    query = select(Order)
    results = await db.execute(query)
    return results.scalars().all()

@router.get("/orders/{order_id}", response_model=OrderCreate)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a single order by UUID."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders/status/{status}", response_model=list[OrderCreate])
async def get_orders_by_status(status: str, db: AsyncSession = Depends(get_db)):
    """Retrieve all orders of a specific status."""
    query = select(Order).where(Order.status == status)
    results = await db.execute(query)
    return results.scalars().all()

@router.post("/orders", response_model=OrderCreate)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    """Create a new order."""
    new_order = Order(
        user_id=order.user_id,
        status=order.status if order.status is not None else None
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.put("/orders/{order_id}", response_model=OrderUpdate)
async def update_order(
    order_id: UUID,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing order using UUID."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order_data.dict(exclude_unset=True).items():
        setattr(order, key, value)
    await db.commit()
    await db.refresh(order)
    return order

@router.put("/orders/{order_id}/next-status", response_model=OrderUpdate)
async def update_order_status(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Move the order to the next status in the sequence."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    status_flow = ["pending", "preparing", "ready", "completed"]
    
    if order.status == "completed":
        raise HTTPException(status_code=400, detail="Order is already completed")
    
    try:
        next_status = status_flow[status_flow.index(order.status) + 1]
        order.status = next_status
        await db.commit()
        await db.refresh(order)
        return order
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid status transition")

@router.put("/orders/{order_id}/cancel", response_model=OrderUpdate)
async def cancel_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Cancel the order by setting the status to 'cancelled'."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = "cancelled"
    await db.commit()
    await db.refresh(order)
    return order

@router.delete("/orders/{order_id}")
async def delete_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an existing order using UUID."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    await db.commit()
    return {"message": "Order deleted successfully!"}