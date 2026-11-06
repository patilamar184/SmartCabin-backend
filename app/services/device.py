from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.device import Device
import secrets
import uuid

from fastapi import HTTPException
from app.core.security import hash_password


from fastapi import HTTPException
from app.models.visitor import Visitor
from app.models.device_command import DeviceCommand


def update_device_heartbeat(device: Device, db: Session):
    device.is_online = True
    device.last_seen = datetime.now(timezone.utc)

    db.commit()
    db.refresh(device)

    return {
        "message": "Heartbeat received successfully",
        "device_id": device.device_id,
        "is_online": device.is_online,
        "last_seen": device.last_seen
    }

def register_device(owner_id: int, device_name: str, db: Session):
    existing_device = db.query(Device).filter(
        Device.owner_id == owner_id
    ).first()

    if existing_device:
        raise HTTPException(
            status_code=409,
            detail="A device is already registered for this owner"
        )

    device_id = f"ESP32-{uuid.uuid4().hex[:12].upper()}"
    api_key = secrets.token_urlsafe(32)

    device = Device(
        owner_id=owner_id,
        device_id=device_id,
        api_key_hash=hash_password(api_key),
        is_active=True,
        is_online=False
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return {
        "message": "Device registered successfully. Save your API key securely.",
        "device_id": device.device_id,
        "api_key": api_key,
        "is_active": device.is_active,
        "created_at": device.created_at
    }

def get_owner_device(owner_id: int, db: Session):
    device = db.query(Device).filter(
        Device.owner_id == owner_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="No device registered"
        )

    return device

from app.models.device_command import DeviceCommand

def get_pending_commands(device: Device, db: Session):
    commands = db.query(DeviceCommand).filter(
        DeviceCommand.device_id == device.id,
        DeviceCommand.status == "pending"
    ).order_by(
        DeviceCommand.created_at.asc()
    ).all()

    return commands

from datetime import datetime, timezone
from app.schemas.device import DeviceCommandAcknowledge


def acknowledge_command(
    command_id: int,
    data: DeviceCommandAcknowledge,
    device: Device,
    db: Session
):
    command = db.query(DeviceCommand).filter(
        DeviceCommand.id == command_id,
        DeviceCommand.device_id == device.id
    ).first()

    if not command:
        raise HTTPException(
            status_code=404,
            detail="Command not found"
        )

    if command.status != "pending":
        raise HTTPException(
            status_code=409,
            detail="Command has already been processed"
        )

    command.status = data.status
    command.acknowledged_at = datetime.now(timezone.utc)

    if data.status == "completed" and command.command_type == "ENROLL_FINGERPRINT":
        visitor_id = command.payload.get("visitor_id")
        fingerprint_id = (data.result or {}).get("fingerprint_id")

        if fingerprint_id is None:
            raise HTTPException(
                status_code=422,
                detail="Fingerprint ID is required for successful enrollment"
            )

        visitor = db.query(Visitor).filter(
            Visitor.id == visitor_id,
            Visitor.owner_id == device.owner_id,
            Visitor.is_active == True
        ).first()

        if not visitor:
            raise HTTPException(
                status_code=404,
                detail="Visitor not found for enrollment"
            )

        visitor.fingerprint_id = fingerprint_id
        visitor.fingerprint_enrolled = True

    db.commit()

    return {
        "message": "Command acknowledgement received",
        "command_id": command.id,
        "status": command.status
    }

from app.models.access_request import AccessRequest
from app.core.security import verify_password
from datetime import timedelta
from app.schemas import DeviceAuthenticationRequest

def authenticate_visitor(
    data: DeviceAuthenticationRequest,
    device: Device,
    db: Session
):
    query = db.query(Visitor).filter(
        Visitor.owner_id == device.owner_id,
        Visitor.is_active == True
    )

    if data.authentication_method == "fingerprint":
        if data.fingerprint_id is None:
            raise HTTPException(
                status_code=422,
                detail="Fingerprint ID is required"
            )

        visitor = query.filter(
            Visitor.fingerprint_id == data.fingerprint_id,
            Visitor.fingerprint_enrolled == True
        ).first()

    else:
        if data.pin is None:
            raise HTTPException(
                status_code=422,
                detail="PIN is required"
            )

        visitors = query.all()

        visitor = next(
            (
                v for v in visitors
                if verify_password(data.pin, v.pin_hash)
            ),
            None
        )

    if not visitor:
        return {
            "authenticated": False,
            "message": "Invalid visitor credentials"
        }

    now = datetime.now(timezone.utc)

    access_request = AccessRequest(
        owner_id=device.owner_id,
        visitor_id=visitor.id,
        authentication_method=data.authentication_method,
        status="pending",
        created_at=now,
        expires_at=now + timedelta(minutes=5)
    )

    db.add(access_request)
    db.commit()
    db.refresh(access_request)

    return {
        "authenticated": True,
        "message": "Authentication successful. Waiting for owner approval.",
        "access_request_id": access_request.id,
        "visitor_id": visitor.id,
        "visitor_name": visitor.name,
        "status": access_request.status
    }