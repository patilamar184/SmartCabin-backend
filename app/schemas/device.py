from pydantic import BaseModel, Field
from datetime import datetime


class DeviceRegister(BaseModel):
    device_name: str = Field(min_length=2, max_length=100)


class DeviceRegistrationResponse(BaseModel):
    message: str
    device_id: str
    api_key: str
    is_active: bool
    created_at: datetime

class DeviceResponse(BaseModel):
    id: int
    device_id: str
    is_active: bool
    is_online: bool
    last_seen: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}

class DeviceCommandResponse(BaseModel):
    id: int
    command_type: str
    payload: dict
    status: str

    model_config = {"from_attributes": True}