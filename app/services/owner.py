from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.owner import Owner
from app.schemas.owner import OwnerRegister
from app.core.security import hash_password


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