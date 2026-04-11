from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.models import CartItem, Product, User
from app.schemas.schemas import CartItemAdd, CartItemUpdate, CartItemOut, CartOut

router = APIRouter(prefix="/cart", tags=["Cart"])


def _get_cart_total(items: list[CartItem]) -> float:
    return round(sum(item.quantity * item.product.price for item in items), 2)


@router.get("/", response_model=CartOut)
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all cart items with a computed total for the logged-in user."""
    items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    return CartOut(items=items, total=_get_cart_total(items))


@router.post("/", response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    payload: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a product to cart. If already present, increments quantity."""
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_qty < payload.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock_qty} units in stock",
        )

    existing = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id, CartItem.product_id == payload.product_id)
        .first()
    )

    if existing:
        new_qty = existing.quantity + payload.quantity
        if new_qty > product.stock_qty:
            raise HTTPException(status_code=400, detail="Requested quantity exceeds stock")
        existing.quantity = new_qty
        db.commit()
        db.refresh(existing)
        return existing

    cart_item = CartItem(
        user_id=current_user.id,
        product_id=payload.product_id,
        quantity=payload.quantity,
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.put("/{item_id}", response_model=CartItemOut)
def update_cart_item(
    item_id: int,
    payload: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update the quantity of a specific cart item."""
    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    if payload.quantity > item.product.stock_qty:
        raise HTTPException(
            status_code=400,
            detail=f"Only {item.product.stock_qty} units available",
        )

    item.quantity = payload.quantity
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a specific item from cart."""
    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove all items from the user's cart (called after order placement)."""
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
