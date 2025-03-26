from pydantic import BaseModel, field_validator
from uuid import UUID
import re


class RestaurantCreate(BaseModel):
    """Schema for creating a new restaurant."""
    id: UUID | None = None

    name: str
    description: str | None = None
    # Address fields
    phone: str
    address: str
    city: str
    state: str
    zip_code: str

    @field_validator("phone", mode="before")
    @classmethod
    def clean_phone(cls, phone: str) -> str:
        """Remove all non-digit characters from phone number."""
        return re.sub(r"\D", "", phone)

    class Config:
        from_attributes = True


class RestaurantUpdate(BaseModel):
    """Schema for updating a restaurant."""
    id: UUID | None = None

    name: str | None = None
    description: str | None = None
    # Address fields
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None

    @field_validator("phone", mode="before")
    @classmethod
    def clean_phone(cls, phone: str | None) -> str | None:
        """Remove all non-digit characters from phone number."""
        return re.sub(r"\D", "", phone) if phone else None

    class Config:
        from_attributes = True
