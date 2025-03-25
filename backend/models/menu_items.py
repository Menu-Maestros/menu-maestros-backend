from sqlalchemy import Column, String, TIMESTAMP, DECIMAL, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import Base

from datetime import datetime

import uuid


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey(
        "restaurants.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(DECIMAL(10, 2), nullable=False)
    image_url = Column(String)
    category = Column(
        Enum("food", "drink", "other", name="menu_category"),
        nullable=False,
    )
    available = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.now())

    order_items = relationship("OrderItem", back_populates="menu_items")
    restaurant = relationship("Restaurant", back_populates="menu_items")
