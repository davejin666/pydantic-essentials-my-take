from pprint import pprint
from pydantic import BaseModel, ConfigDict, ValidationError

class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_1: int

try:
    m = Model(field_1=1, field_2="a")
except ValidationError as exc:
    pprint(exc, indent=2)

Model.model_config = ConfigDict(extra="allow")

class Model(BaseModel):
    model_config = ConfigDict(extra="allow")

    field_1: int

m = Model(field_1=1, field_2="a", field_3=False)

print(Model.model_fields)
print(m.model_fields_set)
print(m.model_extra)