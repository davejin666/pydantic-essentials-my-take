from pydantic import BaseModel, Field, ValidationError
from pprint import pprint

class Model(BaseModel):
    id_:int = Field(alias="id")
    last_name: str = Field(alias="lastName")

json_str = """
{
    "id": 100,
    "lastName": "Jin"
}
"""

m = Model.model_validate_json(json_str)

pprint(repr(m))
pprint(m.model_dump(by_alias=True))