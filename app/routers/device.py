from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.device_auth import get_current_device
from app.models.device import Device
from app.services.device import update_device_heartbeat

from app.schemas.device import DeviceRegister, DeviceRegistrationResponse
from app.dependencies.auth import get_current_owner
from app.services.device import register_device

from app.schemas.device import DeviceResponse
from app.services.device import get_owner_device
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


@router.post(
    "/register",
    response_model=DeviceRegistrationResponse,
    status_code=201
)
def create_device(
    data: DeviceRegister,
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return register_device(
        owner_id=current_owner.id,
        device_name=data.device_name,
        db=db
    )

@router.get("/my-device", response_model=DeviceResponse)
def my_device(
    db: Session = Depends(get_db),
    current_owner=Depends(get_current_owner)
):
    return get_owner_device(current_owner.id, db)