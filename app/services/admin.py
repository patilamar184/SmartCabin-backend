from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.schemas.owner import AdminLogin
from app.core.security import verify_password, create_access_token
from app.models.owner import Owner
from fastapi import HTTPException

from sqlalchemy.orm import Session
from fastapi import HTTPException


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

def get_owner_by_id(owner_id: int, db: Session):
    owner = db.query(Owner).filter(
        Owner.id == owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Cabin Owner not found"
        )

    return owner

from app.schemas.owner import OwnerStatusUpdate


def update_owner_status(
    owner_id: int,
    data: OwnerStatusUpdate,
    db: Session
):
    owner = db.query(Owner).filter(
        Owner.id == owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Cabin Owner not found"
        )

    owner.is_active = data.is_active

    db.commit()
    db.refresh(owner)

    return owner

def delete_owner(owner_id: int, db: Session):
    owner = db.query(Owner).filter(
        Owner.id == owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Cabin Owner not found"
        )

    db.delete(owner)
    db.commit()

    return {
        "message": "Cabin Owner deleted successfully"
    }