from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    id: UUID | None = None
    name: str 
    email: str
    user_type: str # "customer", "restaurant_worker" and "admin"

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    id: UUID | None = None
    name: str | None = None
    email: str | None = None
    user_type: str | None = None # "customer", "restaurant_worker" and "admin"

    class Config:
        from_attributes = True