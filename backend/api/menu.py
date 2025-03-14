from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.database import get_db
from backend.models.menu import MenuItem

from backend.schemas.menu import MenuItemCreate, MenuItemUpdate

from uuid import UUID

router = APIRouter()

@router.get("/menu/", response_model=list[MenuItemCreate])
async def get_menu(db: AsyncSession = Depends(get_db)):
    """Retrieve all menu items."""
    result = await db.execute(select(MenuItem))
    menu_items = result.scalars().all()
    return menu_items

@router.get("/menu/{item_id}", response_model=MenuItemCreate)
async def get_menu_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a single menu item by UUID."""
    item = await db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/menu/")
async def add_menu_item(item: MenuItemCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Create a new menu item
        new_item = MenuItem(
            name=item.name,
            description=item.description,
            price=item.price,
            image_url=item.image_url,
            category=item.category
        )

        # Add to database
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)

        return {"message": "Menu item added successfully!", "item": new_item}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding menu item: {str(e)}")
    
@router.put("/menu/{item_id}", response_model=MenuItemCreate)
async def update_menu_item(
    item_id: UUID, 
    item_data: MenuItemUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Update an existing menu item using UUID."""
    item = await db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item_data.dict(exclude_unset=True).items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/menu/{item_id}")
async def delete_menu_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a menu item from the database using UUID."""
    item = await db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(item)
    await db.commit()

    return {"message": "Menu item deleted successfully"}

