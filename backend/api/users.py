from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from backend.database import get_db
from backend.models.users import User
from backend.schemas.users import UserCreate, UserUpdate

router = APIRouter()

@router.get("/users/", response_model=list[UserUpdate], tags=["Users Endpoints"])
async def get_users(db: AsyncSession = Depends(get_db)):
    """Retrieve all users."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/users/{user_id}", response_model=UserUpdate, tags=["Users Endpoints"])
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a single user by UUID."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/type/{user_type}", response_model=list[UserUpdate], tags=["Users Endpoints"])
async def get_users_by_type(user_type: str, db: AsyncSession = Depends(get_db)):
    """Retrieve all users of a specific type."""
    result = await db.execute(select(User).where(User.user_type == user_type))
    users = result.scalars().all()
    return users

@router.post("/users/", response_model=UserCreate, tags=["Users Endpoints"])
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Create a new user
        new_user = User(
            name=user.name,
            email=user.email,
            user_type=user.user_type
        )
        
        # Add to database
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")

@router.put("/users/{user_id}", response_model=UserUpdate, tags=["Users Endpoints"])
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing user using UUID."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/users/{user_id}", tags=["Users Endpoints"])
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a user from the database using UUID."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"message": "User deleted successfully"}
