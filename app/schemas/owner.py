from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime


class OwnerRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    phone: str | None = None


class OwnerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class OwnerLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class OwnerStatusUpdate(BaseModel):
    is_active: bool