from typing import Annotated, Any
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ValidationError, Field, BeforeValidator, AfterValidator
from dateutil import parser

def parse_dt_str(value: Any):
    if isinstance(value, str):
        try:
            dt = parser.parse(value)
        except Exception as exc:
            raise ValueError(str(exc))
        
        return dt
    return value

def make_aware_dt(dt: datetime):
    if datetime.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt

AwareDateTime = Annotated[
    datetime, 
    BeforeValidator(parse_dt_str), 
    Field(ge=datetime(1988, 7, 16, 2, 10, tzinfo=timezone.utc)),
    AfterValidator(make_aware_dt)
]

class Model(BaseModel):
    dt: AwareDateTime

seoul_now = datetime.now(tz=ZoneInfo("Asia/Seoul"))

m1 = Model(dt=datetime.now(tz=ZoneInfo("Asia/Seoul")))
print(seoul_now)
print(m1.dt)