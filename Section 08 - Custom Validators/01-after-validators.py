from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, ValidationError

class Model(BaseModel):
    dt: datetime = Field(ge=datetime(1988,7,16))

    @field_validator("dt")
    @classmethod
    def aware_dt(cls, dt: datetime):
        print("After validator: ", dt)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt= dt.astimezone(timezone.utc)

        return dt
    
local_now = datetime.now()
seoul_now = datetime.now(tz=ZoneInfo("Asia/Seoul"))

print(local_now, local_now.tzinfo)
print(seoul_now, seoul_now.tzinfo)
print(seoul_now.isoformat())

m1 = Model(dt=local_now)
print(repr(m1.dt))

m2 = Model(dt=seoul_now)
print(repr(m2.dt))

m3 = Model(dt=seoul_now.isoformat())
print(repr(m3.dt))

class Model2(BaseModel):
    num: Annotated[float, Field(gt=0.0, validate_default=True)]

    @field_validator("*")
    @classmethod
    def after_validator1(cls, num: float):
        print(f"Adding 1 to {num=}.")
        num += 1
        return num
    
    @field_validator("*")
    @classmethod
    def after_validator2(cls, num: float):
        print(f"Adding 2 to {num=}.")
        num += 2
        return num

    @field_validator("*")
    @classmethod
    def after_validator3(cls, num: float):
        print(f"Adding 3 to {num=}.")
        num += 3
        return num
    
m4 = Model2(num="1")
print(repr(m4))
    