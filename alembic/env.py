from sqlalchemy import create_engine
from backend.config import settings

from backend.models.base import Base

from backend.models.restaurants import Restaurant
from backend.models.menu_items import MenuItem
from backend.models.orders import Order
from backend.models.users import User
from backend.models.order_items import OrderItem

from alembic import context

SYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql+asyncpg", "postgresql")

engine = create_engine(SYNC_DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_online():
    """Run migrations in 'online' mode with proper connection handling."""
    with engine.begin() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        context.run_migrations()


run_migrations_online()
