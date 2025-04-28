from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.database import get_db

from backend.models.orders import Order
from backend.models.order_items import OrderItem

from backend.schemas.orders import OrderCreate, OrderCreateWithItems, OrderUpdate
from backend.schemas.order_items import OrderItemCreate

from backend.security import require_user_type

from uuid import UUID


router = APIRouter(
    prefix="/restaurants/{restaurant_id}",
    tags=["Orders Endpoints"]
)


@router.get("/orders", response_model=list[OrderCreate])
async def get_orders(restaurant_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve all orders for a restaurant."""
    query = select(Order).where(Order.restaurant_id == restaurant_id)
    results = await db.execute(query)
    return results.unique().scalars().all()


@router.get("/users/{user_id}/orders", response_model=list[OrderCreate])
async def get_orders(
    restaurant_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(
        require_user_type(["admin", "restaurant_worker", "customer"])
    )
):
    """Retrieve all orders by restaurant by user."""
    if current_user["user_type"] == "customer":
        user_id = current_user["user_id"]

    query = select(Order).where(Order.restaurant_id ==
                                restaurant_id).where(Order.user_id == user_id)
    results = await db.execute(query)
    return results.unique().scalars().all()


@router.get("/users/{user_id}/orders/{order_id}", response_model=OrderCreate)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a single order by UUID."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/users/{user_id}/orders/{order_id}/items", response_model=list[OrderItemCreate])
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve order items for a given order."""
    query = select(OrderItem).where(OrderItem.order_id == order_id)
    results = await db.execute(query)
    return results.unique().scalars().all()


@router.get("/status/{status}/orders", response_model=list[OrderCreate])
async def get_orders_by_status(restaurant_id: UUID, status: str, db: AsyncSession = Depends(get_db)):
    """Retrieve all orders of a specific status."""
    query = select(Order)\
        .where(Order.restaurant_id == restaurant_id)\
        .where(Order.status == status)
    results = await db.execute(query)
    return results.scalars().all()


@router.post("/users/{user_id}/orders", response_model=OrderCreateWithItems)
async def create_order_with_items(restaurant_id: UUID, user_id: UUID, order_data: OrderCreateWithItems, db: AsyncSession = Depends(get_db)):
    """Create an order along with its order items in a single transaction."""
    new_order = Order(
        user_id=user_id,
        restaurant_id=restaurant_id,
        name=order_data.name
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


@router.put("/users/{user_id}/orders/{order_id}", response_model=OrderUpdate)
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


@router.put("/users/{user_id}/orders/{order_id}/next-status", response_model=OrderUpdate)
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


@router.put("/users/{user_id}/orders/{order_id}/cancel", response_model=OrderUpdate)
async def cancel_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Cancel the order by setting the status to 'cancelled'."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "cancelled"
    await db.commit()
    await db.refresh(order)
    return order


@router.delete("/users/{user_id}/orders/{order_id}")
async def delete_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an existing order using UUID."""
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await db.delete(order)
    await db.commit()

    return {"message": "Order and order items deleted successfully!"}
