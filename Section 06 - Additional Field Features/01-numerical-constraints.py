from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    dt: datetime = Field(default_factory=datetime.now, lt=datetime(2025, 12, 31))
    tpl: tuple[int, ...] | None = Field(default=None, lt=(10, ))

m1 = Model(dt=datetime(2025, 12, 30))
print(repr(m1))

try:
    Model(dt=datetime(2026, 1, 1))
except ValidationError as exc:
    print(exc)

try:
    Model(tpl = (12, 1, 1, 1))
except ValidationError as exc:
    print(exc)