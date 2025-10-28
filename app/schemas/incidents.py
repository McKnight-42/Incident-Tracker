from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class IncidentBase(BaseModel):
    service_id: int = Field(..., description="ID of the associated service")
    description: str = Field(..., max_length=100)
    start_time: Optional[datetime] = None
    resolved_time: Optional[datetime] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentRead(IncidentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
