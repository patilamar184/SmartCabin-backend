from sqlalchemy.orm import Session
from app.models.access_log import AccessLog


def get_access_logs(owner_id: int, db: Session):
    return db.query(AccessLog).filter(
        AccessLog.owner_id == owner_id
    ).order_by(
        AccessLog.created_at.desc()
    ).all()