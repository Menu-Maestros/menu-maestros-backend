from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.database import get_db
from backend.models.restaurants import Restaurant
from backend.schemas.restaurants import RestaurantCreate, RestaurantUpdate
from uuid import UUID

router = APIRouter()


@router.get("/restaurants/", response_model=list[RestaurantUpdate], tags=["Restaurant Endpoints"])
async def get_restaurants(db: AsyncSession = Depends(get_db)):
    """Retrieve all restaurants."""
    result = await db.execute(select(Restaurant))
    restaurants = result.scalars().all()
    return restaurants


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantUpdate, tags=["Restaurant Endpoints"])
async def get_restaurant(restaurant_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a single restaurant by UUID."""
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.post("/restaurants/", response_model=RestaurantCreate, tags=["Restaurant Endpoints"])
async def add_restaurant(restaurant: RestaurantCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_restaurant = Restaurant(
            name=restaurant.name,
            phone=restaurant.phone,
            address=restaurant.address,
            city=restaurant.city,
            state=restaurant.state,
            zip_code=restaurant.zip_code,
            description=restaurant.description
        )
        db.add(new_restaurant)
        await db.commit()
        await db.refresh(new_restaurant)
        return new_restaurant
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding restaurant: {str(e)}")


@router.put("/restaurants/{restaurant_id}", response_model=RestaurantUpdate, tags=["Restaurant Endpoints"])
async def update_restaurant(
    restaurant_id: UUID,
    restaurant_data: RestaurantUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing restaurant using UUID."""
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    for key, value in restaurant_data.dict(exclude_unset=True).items():
        setattr(restaurant, key, value)

    await db.commit()
    await db.refresh(restaurant)
    return restaurant


@router.delete("/restaurants/{restaurant_id}", tags=["Restaurant Endpoints"])
async def delete_restaurant(restaurant_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a restaurant from the database using UUID."""
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    await db.delete(restaurant)
    await db.commit()
    return {"message": "Restaurant deleted successfully"}
