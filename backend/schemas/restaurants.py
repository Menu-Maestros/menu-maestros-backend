from pydantic import BaseModel
from uuid import UUID


class RestaurantCreate(BaseModel):
    """Schema for creating a new user."""
    id: UUID | None = None

    name: str
    description: str | None = None
    # Address fields
    address: str
    city: str
    state: str
    zip_code: str

    class Config:
        from_attributes = True
