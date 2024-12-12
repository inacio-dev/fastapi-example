from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ...database import get_db
from ...utils.logger import log_info, log_error
from ...models import base as base_models
from ...schemas import base as base_schemas
from ...utils.cache import custom_cache


router = APIRouter()


@router.post("/items", response_model=base_schemas.Item)
@custom_cache(expire=60)
async def create_item(request: Request, item: base_schemas.ItemCreate, db: Session = Depends(get_db)):
    try:
        db_item = base_models.Item(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        log_info(f"Item created: {db_item.id}")
        return db_item
    except Exception as e:
        log_error(f"Error creating item: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/items", response_model=list[base_schemas.Item])
@custom_cache(expire=30)
async def read_items(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        items = db.query(base_models.Item).offset(skip).limit(limit).all()
        log_info(f"Retrieved {len(items)} items")
        return items
    except Exception as e:
        log_error(f"Error retrieving items: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
