from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models import models
from app.core.dependencies import get_current_user  # ✅ IMPORTANT

router = APIRouter()


@router.get("/")
def recommend_products(
    current_user: models.User = Depends(get_current_user),  # ✅ from JWT
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):

    # Get user from token
    user = db.query(models.User).filter(
        models.User.email == current_user.email
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id 

    # Get ordered products
    ordered_products = db.query(models.OrderItem.product_id).join(
        models.Order,
        models.OrderItem.order_id == models.Order.id
    ).filter(models.Order.user_id == user_id).all()

    ordered_ids = [p[0] for p in ordered_products]

    # Get categories of ordered products
    category_ids = []
    if ordered_ids:
        categories = db.query(models.Product.category_id).filter(
            models.Product.id.in_(ordered_ids)
        ).distinct().all()

        category_ids = [c[0] for c in categories]

    recommendations = []

    # Logic 1: Similar category
    if category_ids:
        recommendations = db.query(models.Product).filter(
            models.Product.category_id.in_(category_ids),
            ~models.Product.id.in_(ordered_ids),
            models.Product.stock_qty > 0
        ).limit(limit).all()

    # Logic 2: Top-rated
    if not recommendations:
        recommendations = db.query(models.Product).join(
            models.Review,
            models.Product.id == models.Review.product_id
        ).group_by(models.Product.id).order_by(
            func.avg(models.Review.rating).desc()
        ).limit(limit).all()

    # Logic 3: Latest
    if not recommendations:
        recommendations = db.query(models.Product).order_by(
            models.Product.created_at.desc()
        ).limit(limit).all()

    # Count
    total_available = len(recommendations)

    message = None
    if limit > total_available:
        message = f"Currently we can only recommend {total_available} products"

    return {
        "message": message,
        "count": total_available,
        "data": recommendations
    }