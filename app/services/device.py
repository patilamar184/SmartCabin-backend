from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.device import Device
import secrets
import uuid

from fastapi import HTTPException
from app.core.security import hash_password

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