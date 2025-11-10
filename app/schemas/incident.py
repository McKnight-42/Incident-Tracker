from typing import Annotated
from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationInfo,
    StringConstraints,
    field_validator,
    Field,
)
from typing import Optional
from datetime import datetime


class IncidentBase(BaseModel):
    service_id: int
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
    ]
    start_time: datetime
    resolved_time: Optional[datetime] = None

    @field_validator("resolved_time")
    @classmethod
    def validate_time_order(cls, resolved_time, info: ValidationInfo):
        start_time = info.data.get("start_time")
        if resolved_time and start_time and resolved_time < start_time:
            raise ValueError("resolved_time cannot be before start_time")
        return resolved_time


class IncidentCreate(BaseModel):
    service_id: int
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
    ]
    start_time: datetime = Field(default_factory=datetime.now)
    resolved_time: Optional[datetime] = None

    @field_validator("resolved_time")
    @classmethod
    def validate_time_order(cls, resolved_time, info: ValidationInfo):
        start_time = info.data.get("start_time")
        if resolved_time and start_time and resolved_time < start_time:
            raise ValueError("resolved_time cannot be before start_time")
        return resolved_time


class IncidentRead(IncidentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
