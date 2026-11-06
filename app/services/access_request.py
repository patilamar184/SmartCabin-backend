from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.access_request import AccessRequest


def get_pending_requests(owner_id: int, db: Session):
    return db.query(AccessRequest).filter(
        AccessRequest.owner_id == owner_id,
        AccessRequest.status == "pending"
    ).order_by(
        AccessRequest.created_at.desc()
    ).all()