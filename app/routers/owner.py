from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.owner import OwnerRegister, OwnerResponse
from app.services.owner import register_owner

router = APIRouter(
    prefix="/api/owner",
    tags=["Owner"]
)


@router.post(
    "/register",
    response_model=OwnerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_owner(
    data: OwnerRegister,
    db: Session = Depends(get_db)
):
    return register_owner(data, db)