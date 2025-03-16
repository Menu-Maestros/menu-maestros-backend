import uuid
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from backend.models.base import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    category = Column(String, nullable=False)  # e.g., "food", "drink"
    available = Column(Boolean, default=True, nullable=False)
