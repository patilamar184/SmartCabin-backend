from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.owner import OwnerResponse
from app.dependencies.auth import get_current_admin
from app.services.admin import get_all_owners

from app.services.admin import get_owner_by_id

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)


@router.get(
    "/owners",
    response_model=list[OwnerResponse]
)
def list_owners(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return get_all_owners(db)

@router.get(
    "/owners/{owner_id}",
    response_model=OwnerResponse
)
def owner_details(
    owner_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return get_owner_by_id(owner_id, db)