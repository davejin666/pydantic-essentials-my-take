from pydantic import BaseModel, ConfigDict, ValidationError, Field

class Model(BaseModel):
    model_config = ConfigDict(strict=False)

    field_1: str
    field_2: float
    field_3: list[int]
    field_4: tuple[int, ...]

m = Model(field_1="123", field_2=1, field_3=(1, 2, 3), field_4=["1", "2", "3"])

print(repr(m))