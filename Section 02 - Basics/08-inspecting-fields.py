from pprint import pprint
from typing import Annotated
from pydantic import BaseModel, Field

class Model(BaseModel):
    field_1: int = Field(alias="my_field") # Required, not nullable
    field_2: int | None # Required, nullable
    field_3: int = 1 # Optional, not nullable
    field_4: int | None = None # Optional, nullable

m1 = Model(my_field=1, field_2=None)
m2 = Model(my_field=2, field_2=3, field_4=None)

print(m1.model_fields_set) # {'field_1', 'field_2'}
print(Model.model_fields.keys() - m1.model_fields_set) # {'field_3', 'field_4'}
print(m2.model_fields_set) # {'field_1', 'field_4', 'field_2'}

pprint(m1.model_json_schema(by_alias=False),indent=2)