from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.device_auth import get_current_device
from app.models.device import Device
from app.services.device import update_device_heartbeat

router = APIRouter(
    prefix="/api/device",
    tags=["Device Communication"]
)


@router.post("/heartbeat")
def device_heartbeat(
    db: Session = Depends(get_db),
    current_device: Device = Depends(get_current_device)
):
    return update_device_heartbeat(current_device, db)