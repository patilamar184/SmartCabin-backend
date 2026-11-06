from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.device import Device


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