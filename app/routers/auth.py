from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.owner import OwnerLogin, TokenResponse
from app.services.owner import login_owner
from app.schemas.owner import OwnerResponse
from app.dependencies.auth import get_current_owner

from app.schemas.owner import AdminLogin
from app.services.admin import login_admin











router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/owner/login", response_model=TokenResponse)
def owner_login(
    data: OwnerLogin,
    db: Session = Depends(get_db)
):
    return login_owner(data, db)

@router.get("/owner/me", response_model=OwnerResponse)
def get_owner_profile(
    current_owner = Depends(get_current_owner)
):
    return current_owner


@router.post("/admin/login", response_model=TokenResponse)
def admin_login(
    data: AdminLogin,
    db: Session = Depends(get_db)
):
    return login_admin(data, db)



