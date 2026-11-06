from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.device import Device
from app.core.security import verify_password


def get_current_device(
    device_id: str = Header(..., alias="X-Device-ID"),
    api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    device = db.query(Device).filter(
        Device.device_id == device_id
    ).first()

    if not device or not verify_password(
        api_key, device.api_key_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid device credentials"
        )

    if not device.is_active:
        raise HTTPException(
            status_code=403,
            detail="Device is inactive"
        )

    if not device.owner.is_active:
        raise HTTPException(
            status_code=403,
            detail="Cabin Owner account is inactive"
        )

    return device