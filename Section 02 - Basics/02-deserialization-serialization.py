from pydantic import BaseModel, ValidationError

# Deserialization
class Person(BaseModel):
    first_name: str;
    last_name: str;
    age: int;

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
python_dict = {
    "first_name": "David",
    "last_name": "Jin",
    "age": 38
}

david = Person.model_validate(python_dict) # Deserializes and validates Python dicts and load data into model instances
print(repr(david)) # Person(first_name='David', last_name='Jin', age=38)

json_str = '''
{
    "first_name": "Isaac",
    "last_name": "Newton",
    "age": 84
}
'''

newton = Person.model_validate_json(json_str) # Deserializes and validates JSON strings and load data into model instances
print(repr(newton)) # Person(first_name='Isaac', last_name='Newton', age=84)

# Serialization
dict_newton = newton.model_dump()
print(dict_newton) # {'first_name': 'Isaac', 'last_name': 'Newton', 'age': 84}

dict_newton2 = newton.model_dump(exclude=["age"])
print(dict_newton2) # {'first_name': 'Isaac', 'last_name': 'Newton'}

json_david = david.model_dump_json(indent=2, include=["last_name"])
print(json_david, type(json_david)) # {"last_name": "Jin"} <class 'str'>
