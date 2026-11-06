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