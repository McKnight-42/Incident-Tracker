from pydantic import field_validator, ValidationInfo


class TimeValidationMixin:
    @field_validator("resolved_time")
    @classmethod
    def validate_time_order(cls, resolved_time, info: ValidationInfo):
        start_time = info.data.get("start_time")
        if resolved_time and start_time and resolved_time < start_time:
            raise ValueError("resolved_time cannot be before start_time")
        return resolved_time
