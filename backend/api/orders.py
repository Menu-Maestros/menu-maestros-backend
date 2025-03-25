from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.database import get_db

from backend.models.orders import Order
from backend.models.order_items import OrderItem

from backend.schemas.orders import OrderCreate, OrderCreateWithItems, OrderUpdate

from uuid import UUID


router = APIRouter()


@router.get("/orders", response_model=list[OrderCreate], tags=["Orders Endpoints"])
async def get_orders(db: AsyncSession = Depends(get_db)):
    """Retrieve all orders."""
    query = select(Order)
    results = await db.execute(query)
    return results.unique().scalars().all()


@router.get("/orders/{order_id}", response_model=OrderCreate, tags=["Orders Endpoints"])
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a single order by UUID."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/orders/status/{status}", response_model=list[OrderCreate], tags=["Orders Endpoints"])
async def get_orders_by_status(status: str, db: AsyncSession = Depends(get_db)):
    """Retrieve all orders of a specific status."""
    query = select(Order).where(Order.status == status)
    results = await db.execute(query)
    return results.scalars().all()


@router.post("/orders", response_model=OrderCreateWithItems, tags=["Orders Endpoints"])
async def create_order_with_items(order_data: OrderCreateWithItems, db: AsyncSession = Depends(get_db)):
    """Create an order along with its order items in a single transaction."""
    new_order = Order(
        user_id=order_data.user_id,
        restaurant_id=order_data.restaurant_id
    )

    db.add(new_order)
    await db.flush()

    order_items = [
        OrderItem(order_id=new_order.id, menu_item_id=item.menu_item_id,
                  quantity=item.quantity, price=item.price)
        for item in order_data.order_items
    ]
    db.add_all(order_items)

    await db.commit()
    await db.refresh(new_order)

    return new_order


@router.put("/orders/{order_id}", response_model=OrderUpdate, tags=["Orders Endpoints"])
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


@router.put("/orders/{order_id}/next-status", response_model=OrderUpdate, tags=["Orders Endpoints"])
async def update_order_status(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Move the order to the next status in the sequence."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    status_flow = ["pending", "preparing", "ready", "completed"]

    if order.status == "completed":
        raise HTTPException(
            status_code=400, detail="Order is already completed")

    try:
        next_status = status_flow[status_flow.index(order.status) + 1]
        order.status = next_status
        await db.commit()
        await db.refresh(order)
        return order
    except IndexError:
        raise HTTPException(
            status_code=400, detail="Invalid status transition")


@router.put("/orders/{order_id}/cancel", response_model=OrderUpdate, tags=["Orders Endpoints"])
async def cancel_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Cancel the order by setting the status to 'cancelled'."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "cancelled"
    await db.commit()
    await db.refresh(order)
    return order


@router.delete("/orders/{order_id}", tags=["Orders Endpoints"])
async def delete_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an existing order using UUID."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await db.delete(order)
    await db.commit()

    return {"message": "Order and order items deleted successfully!"}
