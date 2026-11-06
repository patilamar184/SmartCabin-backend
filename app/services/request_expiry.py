from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.access_request import AccessRequest


def expire_pending_requests(db: Session):
    now = datetime.now(timezone.utc)

    expired_requests = db.query(AccessRequest).filter(
        AccessRequest.status == "pending",
        AccessRequest.expires_at <= now
    ).all()

    for request in expired_requests:
        request.status = "expired"

    if expired_requests:
        db.commit()

    return len(expired_requests)