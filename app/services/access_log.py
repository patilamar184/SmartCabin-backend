from sqlalchemy.orm import Session
from app.models.access_log import AccessLog


def get_access_logs(owner_id: int, db: Session):
    return db.query(AccessLog).filter(
        AccessLog.owner_id == owner_id
    ).order_by(
        AccessLog.created_at.desc()
    ).all()

from fastapi import HTTPException


def get_access_log_by_id(
    log_id: int,
    owner_id: int,
    db: Session
):
    log = db.query(AccessLog).filter(
        AccessLog.id == log_id,
        AccessLog.owner_id == owner_id
    ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Access log not found"
        )

    return log