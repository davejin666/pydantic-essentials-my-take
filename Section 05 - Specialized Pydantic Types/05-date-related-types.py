from pydantic import (
    BaseModel,
    ConfigDict,
    PastDatetime,
    FutureDatetime,
    NaiveDatetime,
    AwareDatetime,
    ValidationError
)
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, available_timezones, TZPATH

class Model(BaseModel):
    dt: datetime | None = None
    past: PastDatetime | None = None
    future: FutureDatetime | None = None
    naive: NaiveDatetime | None = None
    aware: AwareDatetime | None = None

local_now = datetime.now() # Naive datetime assumes local time zone.
utc_now = datetime.now(tz=timezone.utc)
# kst = timezone(timedelta(hours=9), name="KST")
korea_now = local_now.astimezone(ZoneInfo("Asia/Seoul"))

print("Local time: ", local_now)
print("Korea time: ", korea_now)

print("Asia/Shanghai" in available_timezones()) # True

m1 = Model(naive=local_now, aware=utc_now)
print(repr(m1))

try:
    Model(aware=local_now)
except ValidationError as exc:
    print(exc) # Input should have timezone info...

m2 = Model(past=local_now-timedelta(hours=1))
print(repr(m2))

m3 = Model(future=korea_now.replace(tzinfo=None))
print(repr(m3))

