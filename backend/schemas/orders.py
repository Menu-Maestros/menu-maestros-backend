from pydantic import BaseModel
from uuid import UUID
from typing import List

from backend.schemas.order_items import OrderItemCreate

class OrderCreate(BaseModel):
    """Schema for creating a new order."""
    id: UUID | None = None
    user_id: UUID
    status: str | None = None # 'pending', 'preparing', 'ready', 'completed' and 'cancelled'

    class Config:
        from_attributes = True

class OrderCreateWithItems(BaseModel):
    id: UUID | None = None
    user_id: UUID
    order_items: List[OrderItemCreate]
    status: str | None = None

class OrderUpdate(BaseModel):
    """Schema for updating an existing order."""
    id: UUID | None = None 
    user_id: UUID | None = None
    status: str # 'pending', 'preparing', 'ready', 'completed' and 'cancelled'

    class Config:
        from_attributes = True