import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.visitor import Visitor
from app.schemas.visitor import VisitorCreate
from app.core.security import hash_password, verify_password
from app.models.device import Device
from app.models.device_command import DeviceCommand

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


from app.schemas.visitor import VisitorUpdate


def update_visitor(
    visitor_id: int,
    owner_id: int,
    data: VisitorUpdate,
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

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(visitor, field, value)

    db.commit()
    db.refresh(visitor)

    return visitor


def delete_visitor(
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

    visitor.is_active = False

    db.commit()

    return {
        "message": "Visitor deactivated successfully"
    }

def initiate_fingerprint_enrollment(
    visitor_id: int,
    owner_id: int,
    db: Session
):
    visitor = db.query(Visitor).filter(
        Visitor.id == visitor_id,
        Visitor.owner_id == owner_id,
        Visitor.is_active == True
    ).first()

    if not visitor:
        raise HTTPException(
            status_code=404,
            detail="Active visitor not found"
        )

    if visitor.fingerprint_enrolled:
        raise HTTPException(
            status_code=409,
            detail="Fingerprint already enrolled"
        )

    device = db.query(Device).filter(
        Device.owner_id == owner_id,
        Device.is_active == True,
        Device.is_online == True
    ).first()

    if not device:
        raise HTTPException(
            status_code=503,
            detail="Cabin device is offline or unavailable"
        )

    command = DeviceCommand(
        device_id=device.id,
        command_type="ENROLL_FINGERPRINT",
        payload={
            "visitor_id": visitor.id,
            "visitor_name": visitor.name
        },
        status="pending"
    )

    db.add(command)
    db.commit()
    db.refresh(command)

    return {
        "message": "Fingerprint enrollment command queued",
        "command_id": command.id,
        "visitor_id": visitor.id,
        "status": command.status
    }