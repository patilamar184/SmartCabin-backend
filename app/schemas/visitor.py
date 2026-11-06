from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Literal


class VisitorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    department: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=10, max_length=15)
    role: Literal["Student", "Teacher"]


class VisitorResponse(BaseModel):
    id: int
    name: str
    department: str
    phone: str
    role: str
    fingerprint_id: int | None
    fingerprint_enrolled: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VisitorRegistrationResponse(VisitorResponse):
    pin: str