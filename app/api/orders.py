from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.models import (
    Order, OrderItem, CartItem, Product, User, Invoice, Alert
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0

    try:
        order = Order(user_id=current_user.id, total_amount=0)
        db.add(order)
        db.flush()  # ✅ get order.id without commit

        for item in cart_items:
            product = item.product

            if product.stock_qty < item.quantity:
                raise HTTPException(status_code=400, detail="Not enough stock")

            product.stock_qty -= item.quantity

            total += item.quantity * product.price

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )
            db.add(order_item)

            if product.stock_qty < 5:
                alert = Alert(
                    product_id=product.id,
                    message=f"Low stock for {product.name}"
                )
                db.add(alert)

        order.total_amount = total

        invoice = Invoice(order_id=order.id, total_amount=total)
        db.add(invoice)

        db.query(CartItem).filter(
            CartItem.user_id == current_user.id
        ).delete()

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "total": total
    }

@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()