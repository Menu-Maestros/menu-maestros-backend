from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from backend.database import get_db
from backend.api.menu import router as menu_router
from backend.api.users import router as user_router
from backend.api.orders import router as order_router

app = FastAPI()

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
    

