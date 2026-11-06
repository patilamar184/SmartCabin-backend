import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.visitor import Visitor
from app.schemas.visitor import VisitorCreate
from app.core.security import hash_password, verify_password


def generate_unique_pin(owner_id: int, db: Session) -> str:
    visitors = db.query(Visitor).filter(
        Visitor.owner_id == owner_id
    ).all()

    existing_hashes = [v.pin_hash for v in visitors]

    for _ in range(100):
        pin = f"{secrets.randbelow(10000):04d}"

        if not any(
            verify_password(pin, pin_hash)
            for pin_hash in existing_hashes
        ):
            return pin

    raise HTTPException(
        status_code=500,
        detail="Unable to generate a unique PIN"
    )


def register_visitor(
    data: VisitorCreate,
    owner_id: int,
    db: Session
):
    pin = generate_unique_pin(owner_id, db)

    visitor = Visitor(
        owner_id=owner_id,
        name=data.name,
        department=data.department,
        phone=data.phone,
        role=data.role,
        pin_hash=hash_password(pin),
        fingerprint_enrolled=False,
        is_active=True
    )

    try:
        db.add(visitor)
        db.commit()
        db.refresh(visitor)
    except Exception:
        db.rollback()
        raise

    return {
        "id": visitor.id,
        "name": visitor.name,
        "department": visitor.department,
        "phone": visitor.phone,
        "role": visitor.role,
        "fingerprint_id": visitor.fingerprint_id,
        "fingerprint_enrolled": visitor.fingerprint_enrolled,
        "is_active": visitor.is_active,
        "created_at": visitor.created_at,
        "pin": pin
    }


def get_all_visitors(owner_id: int, db: Session):
    return db.query(Visitor).filter(
        Visitor.owner_id == owner_id,
        Visitor.is_active == True
    ).order_by(
        Visitor.created_at.desc()
    ).all()

def get_visitor_by_id(
    visitor_id: int,
    owner_id: int,
    db: Session
):
    visitor = db.query(Visitor).filter(
        Visitor.id == visitor_id,
        Visitor.owner_id == owner_id
    ).first()

    if not visitor:
        raise HTTPException(
            status_code=404,
            detail="Visitor not found"
        )

    return visitor