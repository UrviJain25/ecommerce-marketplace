from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_roles
from app.models.models import Product, User, UserRole
from app.schemas.schemas import ProductCreate, ProductUpdate, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductOut])
def list_products(
    category_id: Optional[int] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by product name"),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Public product listing with optional filters:
    - category, name search, price range, pagination
    """
    q = db.query(Product).filter(Product.stock_qty > 0)

    if category_id:
        q = q.filter(Product.category_id == category_id)
    if search:
        q = q.filter(Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)

    return q.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.seller, UserRole.admin)),
):
    """Seller/Admin: add a new product to the catalog."""
    product = Product(**payload.model_dump(), seller_id=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.seller, UserRole.admin)),
):
    """Seller: update own product. Admin: update any product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Sellers can only edit their own products
    if current_user.role == UserRole.seller and product.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own products")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.seller, UserRole.admin)),
):
    """Seller: delete own product. Admin: delete any product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if current_user.role == UserRole.seller and product.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own products")

    db.delete(product)
    db.commit()


@router.get("/seller/my-products", response_model=List[ProductOut])
def my_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.seller, UserRole.admin)),
):
    """Seller: list all products they have listed."""
    return db.query(Product).filter(Product.seller_id == current_user.id).all()
