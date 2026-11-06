from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_owner
from app.schemas.access_log import AccessLogResponse
from app.services.access_log import get_access_logs

router = APIRouter(
    prefix="/api/access-logs",
    tags=["Access Logs"]
)


@router.get("/", response_model=list[AccessLogResponse])
def list_access_logs(
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return get_access_logs(current_owner.id, db)

from app.services.access_log import get_access_log_by_id

@router.get("/{log_id}", response_model=AccessLogResponse)
def access_log_details(
    log_id: int,
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return get_access_log_by_id(
        log_id=log_id,
        owner_id=current_owner.id,
        db=db
    )