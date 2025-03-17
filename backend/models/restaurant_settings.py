from sqlalchemy import Column, String, TIMESTAMP, Integer
from backend.models.base import Base


class RestaurantSetting(Base):
    __tablename__ = "restaurant_settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_key = Column(String, unique=True, nullable=False)
    setting_value = Column(String, nullable=False)
    updated_at = Column(TIMESTAMP, default="now()")