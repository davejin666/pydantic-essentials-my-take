from typing import Annotated, Any
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from dateutil import parser
from pydantic import (
    BaseModel, 
    field_validator, 
    ValidationInfo,
    ValidationError,
    ConfigDict,
    BeforeValidator,
    AfterValidator
)

def parse_dt_str(value: Any):
    if isinstance(value, str):
        try:
            dt = parser.parse(value)
        except Exception as exc:
            raise ValueError(str(exc))
    return value

def make_aware_dt_utc(dt: datetime):
    print("make_aware_dt_utc executing...")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    return dt

AwareDtUTC = Annotated[datetime, BeforeValidator(parse_dt_str), AfterValidator(make_aware_dt_utc)]

class Model(BaseModel):
    model_config = ConfigDict(validate_default=True, validate_assignment=True)

    start_dt: AwareDtUTC
    end_dt: AwareDtUTC

    @field_validator("end_dt")
    @classmethod
    def end_after_start(cls, end_dt: datetime, info: ValidationInfo):
        print("end_after_start executing...")

        if "start_dt" in info.data:
            if end_dt < info.data["start_dt"]:
                raise ValueError("`start_dt` must precede `end_dt`")
        return end_dt

local_now = datetime.now()
seoul_now = datetime.now(ZoneInfo("Asia/Seoul"))
seoul_tomorrow = seoul_now + timedelta(days=1)
seoul_yesterday = seoul_now - timedelta(days=1)

try:
    m1 = Model(start_dt=seoul_tomorrow, end_dt=seoul_now)
except ValidationError as exc:
    print(exc)
else:
    print(repr(m1))

    
