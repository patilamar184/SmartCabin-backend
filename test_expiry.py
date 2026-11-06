from datetime import datetime, timezone, timedelta

from app.database.database import SessionLocal
from app.models.access_request import AccessRequest
from app.services.request_expiry import expire_pending_requests

db = SessionLocal()

try:
    # Find an existing visitor
    visitor = db.query(AccessRequest.visitor.property.mapper.class_).first()

    if not visitor:
        print("No visitor found. Register a visitor first.")
    else:
        request = AccessRequest(
            owner_id=visitor.owner_id,
            visitor_id=visitor.id,
            authentication_method="pin",
            status="pending",
            created_at=datetime.now(timezone.utc) - timedelta(minutes=6),
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1)
        )

        db.add(request)
        db.commit()
        db.refresh(request)

        print("Test request created:", request.id)

        count = expire_pending_requests(db)
        db.refresh(request)

        print("Expired requests:", count)
        print("Request status:", request.status)

finally:
    db.close()