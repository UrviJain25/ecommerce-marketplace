from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.models import Category, UserRole
from app.schemas.schemas import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """List all product categories (public)."""
    return db.query(Category).all()


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat


@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    """Admin only: create a new category."""
    if db.query(Category).filter(Category.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Category already exists")

    if payload.parent_id:
        parent = db.query(Category).filter(Category.id == payload.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    cat = Category(name=payload.name, parent_id=payload.parent_id)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles(UserRole.admin))],
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Admin only: delete a category."""
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
