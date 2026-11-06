from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.owner import OwnerResponse
from app.dependencies.auth import get_current_admin
from app.services.admin import get_all_owners

from app.services.admin import get_owner_by_id

from app.schemas.owner import OwnerStatusUpdate
from app.services.admin import update_owner_status
from fastapi import status


from app.services.admin import delete_owner

from app.schemas.admin import AdminDashboardResponse
from app.services.admin import get_admin_dashboard


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

@router.patch(
    "/owners/{owner_id}/status",
    response_model=OwnerResponse
)
def change_owner_status(
    owner_id: int,
    data: OwnerStatusUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return update_owner_status(owner_id, data, db)

@router.delete("/owners/{owner_id}")
def remove_owner(
    owner_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return delete_owner(owner_id, db)

@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse
)
def admin_dashboard(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return get_admin_dashboard(db)