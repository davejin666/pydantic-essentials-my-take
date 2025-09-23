from pydantic import BaseModel, ValidationError, ConfigDict

class Model(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        strict=True,
        validate_default=True
    )

    field_1: int = None

try:
    m = Model()
except ValidationError as exc:
    print(exc)

class Model(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        strict=True,
        validate_assignment=True
    )

    field_1: int

try:
    m = Model(field_1=100)
    print(repr(m))
    m.field_1 = "888"
except ValidationError as exc:
    print(exc)