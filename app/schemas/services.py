from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from .incidents import IncidentRead


class ServiceBase(BaseModel):
    name: str
    status: str
    last_checked: Optional[datetime] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: int
    incidents: List[IncidentRead] = []

    model_config = ConfigDict(from_attributes=True)
