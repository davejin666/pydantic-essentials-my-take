from pydantic import BaseModel, ConfigDict, Field

class Person(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    id_: int = Field(alias="ID", serialization_alias="id")
    first_name: str = Field(alias="FirstName", serialization_alias="firstName")
    last_name: str = Field(alias="lastName")
    age: int

json_str = """
{
    "ID": 100,
    "FirstName": "David",
    "lastName": "Jin",
    "age": 38
}
"""

david = Person.model_validate_json(json_str)

print(repr(david))
print(david.model_dump(by_alias=True))