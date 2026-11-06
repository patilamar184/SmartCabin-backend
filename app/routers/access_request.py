from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_owner
from app.schemas.access_request import AccessRequestResponse
from app.services.access_request import get_pending_requests

router = APIRouter(
    prefix="/api/access-requests",
    tags=["Access Requests"]
)


@router.get(
    "/",
    response_model=list[AccessRequestResponse]
)
def list_pending_requests(
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return get_pending_requests(
        owner_id=current_owner.id,
        db=db
    )