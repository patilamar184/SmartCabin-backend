from pydantic import BaseModel
from datetime import datetime


class AccessLogResponse(BaseModel):
    id: int
    visitor_id: int | None
    event_type: str
    authentication_method: str | None
    result: str
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}