from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

def make_alias(field_name: str) -> str:
    alias = to_camel(field_name)
    return alias.removesuffix("_")

class Person(BaseModel):
    model_config = ConfigDict(alias_generator=make_alias)

    id_: int
    first_name: str | None = None
    last_name: str
    age: int | None = None

david = Person(id=10, firstName="David", lastName="Jin", age=38)

print(repr(david))
print(david.model_dump(by_alias=True))

