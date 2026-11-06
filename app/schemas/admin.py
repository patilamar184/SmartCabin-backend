from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):
    total_owners: int
    active_owners: int
    blocked_owners: int
    total_visitors: int
    online_devices: int