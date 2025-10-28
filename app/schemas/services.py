from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime
from .incidents import IncidentRead


class ServiceBase(BaseModel):
    name: str = Field(..., max_length=50)
    status: Optional[Literal["operational", "degraded", "down"]] = "operational"
    last_checked: Optional[datetime] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: int
    incidents: List[IncidentRead] = []

    model_config = ConfigDict(from_attributes=True)
