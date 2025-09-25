from pydantic import BaseModel, Field, ConfigDict, ValidationError

class Model(BaseModel):
    model_config = ConfigDict(
        strict=False,
        validate_default=True
    )

    field_1: bool = Field(strict=True)
    field_2: bool

try:
    Model(field_1=1, field_2=1)
except ValidationError as exc:
    print(exc)

m1 = Model(field_1=True, field_2=0)
print(repr(m1))