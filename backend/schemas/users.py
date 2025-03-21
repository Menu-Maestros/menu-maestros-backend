from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    id: UUID | None = None
    name: str 
    email: str
    password: str
    user_type: str  # "customer", "restaurant_worker", "admin"
    active: bool = True

    # Address fields
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    id: UUID | None = None
    name: str | None = None
    email: str | None = None
    # password: str | None = None  # Don't allow password update and don't show in response
    user_type: str | None = None
    active: bool | None = None  # Allow deactivation/reactivation

    # Address fields
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Schema for user login requests."""
    email: str
    password: str  # Provided by the user during login

class UserPasswordUpdate(BaseModel):
    """Schema for updating only the password."""
    old_password: str  # Required to verify current password
    new_password: str  # New password to be set