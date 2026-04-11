from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Invoice

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.get("/{order_id}")
def get_invoice(order_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice