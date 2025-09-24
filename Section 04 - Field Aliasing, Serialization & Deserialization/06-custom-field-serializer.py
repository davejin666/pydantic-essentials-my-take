from datetime import datetime, timezone
from pydantic import BaseModel, field_serializer, FieldSerializationInfo

class Model(BaseModel):
    dt: datetime | None = None

    @field_serializer("dt", when_used="unless-none")
    def dt_serializer(self, dt: datetime, info: FieldSerializationInfo) -> datetime | str:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)

        if info.mode_is_json():
            return dt.strftime("%Y/%m/%d %H-%M-%S %Z")
        else:
            return dt
        
m = Model(dt=datetime(1988, 7, 16, 2, 10))

print(repr(m))
print(m.model_dump())
print(m.model_dump_json())

m2 = Model()
print(m2.model_dump())
print(m2.model_dump_json())