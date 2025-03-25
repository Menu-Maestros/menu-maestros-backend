import logging
from backend.config import settings

logging.basicConfig(
    format="%(levelname)s:     %(asctime)s  - MESSAGE: %(message)s",
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
)

logger = logging.getLogger("FastAPI")
 