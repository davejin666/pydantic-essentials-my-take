from dateutil.parser import parse
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

class Model(BaseModel):
    dt: datetime

    @field_validator("*", mode="before")
    @classmethod
    def validate_dt_string(cls, raw_dt: Any):
        if isinstance(raw_dt, str):
            try:
                dt = parse(raw_dt)
            except Exception as exc:
                raise ValueError(str(exc))
            
            return dt
        return raw_dt
    
    @field_validator("*", mode="after")
    @classmethod
    def conver_to_utc(cls, dt: datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(tz=timezone.utc)
        return dt

try:  
    m1 = Model(dt="1988/7/16 2:10 AM")
except ValidationError as exc:
    print(exc)
else:
    print(repr(m1))
