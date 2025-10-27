from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class IncidentBase(BaseModel):
    service_id: int
    description: str
    start_time: Optional[datetime] = None
    resolved_time: Optional[datetime] = None


class IncidentCreate(IncidentBase):
    pass


class IncidentRead(IncidentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
