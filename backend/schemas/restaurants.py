from pydantic import BaseModel
from uuid import UUID


class RestaurantCreate(BaseModel):
    """Schema for creating a new user."""
    id: UUID | None = None

    name: str
    description: str | None = None
    # Address fields
    phone: str
    address: str
    city: str
    state: str
    zip_code: str

    class Config:
        from_attributes = True


class RestaurantUpdate(BaseModel):
    """Schema for creating a new user."""
    id: UUID | None = None

    name: str
    description: str | None = None
    # Address fields
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None

    class Config:
        from_attributes = True
