from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.access_request import AccessRequest


def get_pending_requests(owner_id: int, db: Session):
    return db.query(AccessRequest).filter(
        AccessRequest.owner_id == owner_id,
        AccessRequest.status == "pending"
    ).order_by(
        AccessRequest.created_at.desc()
    ).all()

from datetime import datetime, timezone

from app.models.device import Device
from app.models.device_command import DeviceCommand

def approve_access_request(
    request_id: int,
    owner_id: int,
    db: Session
):
    access_request = db.query(AccessRequest).filter(
        AccessRequest.id == request_id,
        AccessRequest.owner_id == owner_id
    ).first()

    if not access_request:
        raise HTTPException(
            status_code=404,
            detail="Access request not found"
        )

    now = datetime.now(timezone.utc)

    expires_at = access_request.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if access_request.status != "pending":
        raise HTTPException(
            status_code=409,
            detail="Request has already been processed"
        )

    if expires_at <= now:
        access_request.status = "expired"
        db.commit()
        raise HTTPException(
            status_code=409,
            detail="Access request has expired"
        )

    device = db.query(Device).filter(
        Device.owner_id == owner_id,
        Device.is_active == True,
        Device.is_online == True
    ).first()

    if not device:
        raise HTTPException(
            status_code=503,
            detail="Cabin device is offline"
        )

    access_request.status = "approved"
    access_request.responded_at = now

    command = DeviceCommand(
        device_id=device.id,
        command_type="UNLOCK_DOOR",
        payload={"duration_seconds": 15},
        status="pending"
    )

    db.add(command)
    db.commit()
    db.refresh(access_request)

    return {
        "message": "Access request approved",
        "request_id": access_request.id,
        "status": access_request.status,
        "door_unlock_duration": 15
    }

def deny_access_request(
    request_id: int,
    owner_id: int,
    db: Session
):
    access_request = db.query(AccessRequest).filter(
        AccessRequest.id == request_id,
        AccessRequest.owner_id == owner_id
    ).first()

    if not access_request:
        raise HTTPException(
            status_code=404,
            detail="Access request not found"
        )

    if access_request.status != "pending":
        raise HTTPException(
            status_code=409,
            detail="Request has already been processed"
        )

    now = datetime.now(timezone.utc)

    expires_at = access_request.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= now:
        access_request.status = "expired"
        db.commit()
        raise HTTPException(
            status_code=409,
            detail="Access request has expired"
        )

    access_request.status = "denied"
    access_request.responded_at = now

    db.commit()
    db.refresh(access_request)

    return {
        "message": "Access request denied",
        "request_id": access_request.id,
        "status": access_request.status
    }


def get_access_request_by_id(
    request_id: int,
    owner_id: int,
    db: Session
):
    access_request = db.query(AccessRequest).filter(
        AccessRequest.id == request_id,
        AccessRequest.owner_id == owner_id
    ).first()

    if not access_request:
        raise HTTPException(
            status_code=404,
            detail="Access request not found"
        )

    return access_request