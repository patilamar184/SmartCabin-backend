from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.schemas.owner import AdminLogin
from app.core.security import verify_password, create_access_token
from app.models.owner import Owner

def login_admin(data: AdminLogin, db: Session):
    admin = db.query(Admin).filter(
        Admin.email == data.email
    ).first()

    if not admin or not verify_password(
        data.password, admin.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=403,
            detail="Admin account is inactive"
        )

    token = create_access_token({
        "sub": str(admin.id),
        "role": "admin"
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def get_all_owners(db: Session):
    return db.query(Owner).order_by(
        Owner.created_at.desc()
    ).all()