from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import models
from app.schemas import schemas
from .auth import get_current_user  

router = APIRouter()


@router.post("/reviews", response_model=schemas.ReviewResponse)
def add_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # ✅ GET USER FROM TOKEN
):

    # Check product exists
    product = db.query(models.Product).filter(
        models.Product.id == review.product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Prevent duplicate review
    existing = db.query(models.Review).filter(
        models.Review.user_id == current_user.id,
        models.Review.product_id == review.product_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already reviewed")

    # Rating validation (extra safety)
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    # CREATE REVIEW USING TOKEN USER
    new_review = models.Review(
        user_id=current_user.id,
        product_id=review.product_id,
        rating=review.rating,
        comment=review.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


@router.get("/{product_id}", response_model=list[schemas.ReviewResponse])
def get_reviews(product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reviews = db.query(models.Review).filter(
        models.Review.product_id == product_id
    ).all()

    return reviews