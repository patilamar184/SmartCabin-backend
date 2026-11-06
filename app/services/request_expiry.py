from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.access_request import AccessRequest

from app.services.logging_service import create_access_log


def expire_pending_requests(db: Session):
    now = datetime.now(timezone.utc)

    expired_requests = db.query(AccessRequest).filter(
        AccessRequest.status == "pending",
        AccessRequest.expires_at <= now
    ).all()

    for request in expired_requests:
        request.status = "expired"

        create_access_log(
            db=db,
            owner_id=request.owner_id,
            visitor_id=request.visitor_id,
            event_type="ACCESS_REQUEST",
            result="expired",
            authentication_method=request.authentication_method,
            description="Access request expired because owner did not respond within 5 minutes"
        )

    if expired_requests:
        db.commit()

    return len(expired_requests)