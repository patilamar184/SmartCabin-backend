from sqlalchemy.orm import Session

from app.models.access_log import AccessLog


def create_access_log(
    db: Session,
    owner_id: int,
    visitor_id: int | None,
    event_type: str,
    result: str,
    authentication_method: str | None = None,
    description: str | None = None
):
    log = AccessLog(
        owner_id=owner_id,
        visitor_id=visitor_id,
        event_type=event_type,
        authentication_method=authentication_method,
        result=result,
        description=description
    )

    db.add(log)

    return log