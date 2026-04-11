from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.models import Alert, UserRole
from app.schemas.schemas import AlertOut

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/", response_model=List[AlertOut])
def get_alerts(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.admin)),
):
    """
    Admin only: View all low stock alerts
    """
    return db.query(Alert).order_by(Alert.created_at.desc()).all()