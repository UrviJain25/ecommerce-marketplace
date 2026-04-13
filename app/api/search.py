from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import models

router = APIRouter()

@router.get("/")
def search_products(
    keyword: str = Query(..., min_length=1, max_length=50),
    min_price: float = Query(0, ge=0),
    max_price: float = Query(1000000, ge=0),
    category_id: int | None = Query(None, gt=0),
    db: Session = Depends(get_db)
):

    #Validate price range
    if min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price"
        )

    #Base query
    query = db.query(models.Product)

    #Keyword filter
    query = query.filter(
        models.Product.name.ilike(f"%{keyword}%")
    )

    #Price filter
    query = query.filter(
        models.Product.price >= min_price,
        models.Product.price <= max_price
    )

    #Category validation + filter
    if category_id:
        category = db.query(models.Category).filter(
            models.Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        query = query.filter(models.Product.category_id == category_id)

    #Execute query
    results = query.all()

    # Handle no results
    if not results:
        raise HTTPException(status_code=404, detail="No search results")
    return results
