from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from backend.logger import logger
from backend.database import get_db
from backend.models.users import User
from backend.schemas.users import UserCreate, UserUpdate, UserLogin, UserPasswordUpdate

from backend.security import hash_password, pwd_context, verify_password, create_access_token, require_user_type

router = APIRouter()


@router.get("/users/", response_model=list[UserUpdate], tags=["Users Endpoints"])
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(
        require_user_type(["admin", "restaurant_worker"])
    )
):
    """Retrieve all users."""
    logger.debug(
        f"Restricted for user type admin or restaurant worker: {current_user}")
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/users/{user_id}", response_model=UserUpdate, tags=["Users Endpoints"])
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(
        require_user_type(["admin", "restaurant_worker"])
    )
):
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


@router.post("/register/", response_model=UserUpdate, tags=["Users Endpoints"])
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Hash the user's password before storing it
        hashed_password = hash_password(user.password)

        # Create a new user
        new_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            user_type=user.user_type,
            active=user.active,
            address=user.address,
            city=user.city,
            state=user.state,
            zip_code=user.zip_code
        )

        # Add to database
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding user: {str(e)}")


@router.post("/login/", tags=["Users Endpoints"])
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token."""
    result = await db.execute(select(User).where(User.email == user.email))
    user_db = result.scalars().first()

    if not user_db or not verify_password(user.password, user_db.password):
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

    if not user_db.active:
        raise HTTPException(status_code=403, detail="User account is inactive")

    # Generate JWT token
    token_data = {"sub": user_db.email, "user_id": str(
        user_db.id), "user_type": user_db.user_type}
    access_token = create_access_token(token_data)

    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/users/{user_id}/password", tags=["Users Endpoints"])
async def update_password(
    user_id: UUID,
    password_data: UserPasswordUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update user password after verifying the old password."""
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(password_data.old_password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect old password")

    # Hash the new password and update it
    user.password = hash_password(password_data.new_password)

    await db.commit()
    return {"message": "Password updated successfully"}


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
