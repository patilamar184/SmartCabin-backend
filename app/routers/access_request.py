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

from app.services.access_request import approve_access_request

@router.post("/{request_id}/allow")
def allow_access(
    request_id: int,
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return approve_access_request(
        request_id=request_id,
        owner_id=current_owner.id,
        db=db
    )

from app.services.access_request import deny_access_request

@router.post("/{request_id}/deny")
def deny_access(
    request_id: int,
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return deny_access_request(
        request_id=request_id,
        owner_id=current_owner.id,
        db=db
    )


from app.services.access_request import get_access_request_by_id

@router.get("/{request_id}")
def access_request_details(
    request_id: int,
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return get_access_request_by_id(
        request_id=request_id,
        owner_id=current_owner.id,
        db=db
    )