from sqlalchemy import Column, String, TIMESTAMP, DECIMAL, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import Base

from datetime import datetime

import uuid


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey(
        "orders.id", ondelete="CASCADE"))
    menu_item_id = Column(UUID(as_uuid=True), ForeignKey(
        "menu_items.id", ondelete="CASCADE"))

    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())

    order = relationship("Order", back_populates="order_items", lazy="joined")
    menu_item = relationship(
        "MenuItem", back_populates="order_items", lazy="joined")
