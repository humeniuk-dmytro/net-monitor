from datetime import datetime
from pydantic import BaseModel, ConfigDict


class HostCreate(BaseModel):
    hostname: str
    ip: str | None = None


class HostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    hostname: str
    ip: str | None
    is_active: bool
    created_at: datetime


class StatsRead(BaseModel):
    host_id: int
    period: str
    count: int
    avg_ms: float | None
    min_ms: float | None
    max_ms: float | None
    p95_ms: float | None