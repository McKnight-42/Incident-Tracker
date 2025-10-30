from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from .incident import IncidentRead


class ServiceBase(BaseModel):
    name: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)
    ]
    status: Literal["operational", "degraded", "down"] = "operational"
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
