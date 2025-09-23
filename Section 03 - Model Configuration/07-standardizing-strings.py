from pydantic import BaseModel, ConfigDict

class Model(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_to_lower=True,
        coerce_numbers_to_str=True
    )

    field_1: str
    field_2: str
    field_3: int


m1 = Model(field_1="               PyThon  \t\n", field_2=123456, field_3="   123 ")
m2 = Model(field_1="       pytHON \t\t", field_2=123456, field_3="123 ")

print(repr(m1), repr(m2))
print(m1 == m2)