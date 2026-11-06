from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.owner import Owner
from app.schemas.owner import OwnerRegister
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token
from app.schemas.owner import OwnerLogin

def register_owner(data: OwnerRegister, db: Session):

    existing_owner = db.query(Owner).filter(
        Owner.email == data.email
    ).first()

    if existing_owner:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_owner = Owner(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        phone=data.phone
    )

    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)

    return new_owner

def login_owner(data: OwnerLogin, db: Session):

    owner = db.query(Owner).filter(
        Owner.email == data.email
    ).first()

    if not owner or not verify_password(
        data.password, owner.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not owner.is_active:
        raise HTTPException(
            status_code=403,
            detail="Your account is inactive"
        )

    access_token = create_access_token({
        "sub": str(owner.id),
        "role": "owner"
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }