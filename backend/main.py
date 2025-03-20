from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.security import APIKeyHeader

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from backend.database import get_db

from backend.config import settings

from backend.api.menu import router as menu_router
from backend.api.users import router as user_router
from backend.api.orders import router as order_router

app = FastAPI()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("Authorization")
    if api_key != f"{settings.API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await call_next(request)

app.include_router(menu_router)
app.include_router(user_router)
app.include_router(order_router)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"error": str(e)}
    

