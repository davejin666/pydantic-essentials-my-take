from enum import Enum
from pydantic import BaseModel, ConfigDict

class Color(Enum):
    R = "Red"
    G = "Green"
    B = "Blue"

class Model(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        str_to_upper=True
    )

    color: Color

m1 = Model(color="Red")
m2 = Model(color=Color.G)

print(repr(m1), repr(m2))

json_str = """
{"color":"Blue"}
"""

m3 = Model.model_validate_json(json_str)
print(repr(m3))

# Enum field after serialization
print(m1.model_dump(), type(m1.color))