from pydantic import BaseModel, ConfigDict, ValidationError, Field
from pydantic.alias_generators import to_camel

class Person(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        alias_generator=to_camel
    )

    id_: int = Field(alias="id")
    first_name: str | None = None
    last_name: str
    age: int | None = None

david = Person(id=100, firstName="David", lastName="Jin", age=38)

print(repr(david))
print(david.model_dump())
print(david.model_dump(by_alias=True))

json_str = """
{
    "id": 200,
    "firstName": "Issac",
    "lastName": "Newton",
    "age": 68
}
"""

newton = Person.model_validate_json(json_str)

print(repr(newton))
print(newton.model_dump_json(by_alias=True))

class NewPerson(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        alias_generator=to_camel
    )

    id_: int = Field(alias="id")
    first_name: str | None = None
    last_name: str
    age: int | None = None

bach = NewPerson(id=300, firstName="Johanes", last_name="Bach", age=58)

print(repr(bach))
print(bach.model_dump(by_alias=True))