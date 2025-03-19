from pydantic import BaseModel
from uuid import UUID

class OrderCreate(BaseModel):
    """Schema for creating a new order."""
    id: UUID | None = None
    user_id: UUID
    status: str | None = None # 'pending', 'preparing', 'ready', 'completed' and 'cancelled'

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    """Schema for updating an existing order."""
    id: UUID | None = None 
    user_id: UUID | None = None
    status: str # 'pending', 'preparing', 'ready', 'completed' and 'cancelled'

    class Config:
        from_attributes = True