from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class OrderItemCreate(BaseModel):
    """Schema for creating order items."""
    id: UUID | None = None
    order_id: UUID | None = None
    menu_item_id: UUID
    quantity: int
    price: Decimal

    class Config:
        from_attributes = True


class OrderItemUpdate(BaseModel):
    """Schema for updating an existing order."""
    id: UUID | None = None
    order_id: UUID | None = None
    menu_item_id: UUID | None = None
    quantity: int | None = None
    price: Decimal | None = None

    class Config:
        from_attributes = True
