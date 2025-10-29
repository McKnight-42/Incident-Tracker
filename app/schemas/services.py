from pydantic import BaseModel, ConfigDict, constr, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from .incidents import IncidentRead


class ServiceBase(BaseModel):
    name: str = constr(strip_whitespace=True, min_length=1, max_length=50)
    status: Optional[Literal["operational", "degraded", "down"]] = "operational"
    last_checked: Optional[datetime] = None

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("name must not be empty or whitespace")
        return v


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: int
    incidents: List[IncidentRead] = []

    model_config = ConfigDict(from_attributes=True)
