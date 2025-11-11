from typing import Annotated
from pydantic import (
    BaseModel,
    ConfigDict,
    StringConstraints,
    Field,
)
from typing import Optional
from datetime import datetime, UTC
from .mixins import TimeValidationMixin


class IncidentBase(BaseModel):
    service_id: int
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
    ]
    start_time: datetime
    resolved_time: Optional[datetime] = None


class IncidentCreate(BaseModel, TimeValidationMixin):
    service_id: int
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
    ]
    start_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resolved_time: Optional[datetime] = None


class IncidentRead(IncidentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
