from pprint import pprint
from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    first_name: str;
    last_name: str;
    age: int;

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
david = Person(first_name="David", last_name="Jin", age=38)

print(repr(david)) # Person(first_name='David', last_name='Jin', age=38)
print(Person.model_fields)

try:
    # Invalid field value
    Person()
except ValidationError as ex:
    pprint(ex.errors(include_url=False)[0], indent=4)

david.age = "thirty-eight" # By default, model instances don't validate reassigned value.
print(repr(david))