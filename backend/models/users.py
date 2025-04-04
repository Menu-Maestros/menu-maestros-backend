from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import Base

from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey(
        "restaurants.id", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # Hashed password
    user_type = Column(String, nullable=False)
    active = Column(Boolean, default=True)  # Soft delete
    created_at = Column(TIMESTAMP, default=datetime.now())

    # Address fields
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)

    orders = relationship("Order", back_populates="user")
    restaurant = relationship("Restaurant", back_populates="users")
