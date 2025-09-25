from typing import Annotated, TypeVar
from pydantic import BaseModel, Field, ValidationError

EleType = TypeVar("EleType")
AnotherType = TypeVar("AnotherType")

ConstrainedList = Annotated[list[EleType | AnotherType], Field(min_length=2, max_length=6)]

class Model(BaseModel):
    field_1: ConstrainedList[str, int]

try:
    m1 = Model(field_1=[1, 2, 3])
except ValidationError as exc:
    print(exc)