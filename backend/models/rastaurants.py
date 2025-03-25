from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from backend.models.base import Base
import uuid


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    description = Column(String)

    # Relationships
    menu_items = relationship(
        "MenuItem", back_populates="restaurants", cascade="all, delete")
    orders = relationship(
        "Order", back_populates="restaurants", cascade="all, delete")
    users = relationship(
        "User", back_populates="restaurants", cascade="all, delete")
