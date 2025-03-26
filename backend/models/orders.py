from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import Base

from datetime import datetime

import uuid


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey(
        "restaurants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="SET NULL"))

    name = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(TIMESTAMP, default=datetime.now())

    user = relationship("User", back_populates="orders", lazy="joined")
    order_items = relationship(
        "OrderItem", back_populates="order", lazy="joined", cascade="all, delete-orphan")
    restaurant = relationship(
        "Restaurant", back_populates="orders", lazy="joined")
