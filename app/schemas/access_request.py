from pydantic import BaseModel
from datetime import datetime


class AccessRequestResponse(BaseModel):
    id: int
    visitor_id: int
    authentication_method: str
    status: str
    created_at: datetime
    expires_at: datetime

    model_config = {"from_attributes": True}