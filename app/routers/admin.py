from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.owner import OwnerResponse
from app.dependencies.auth import get_current_admin
from app.services.admin import get_all_owners

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