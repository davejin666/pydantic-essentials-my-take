from typing import Annotated
from pydantic import BaseModel, ConfigDict, ValidationError, Field, StringConstraints

class Model(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=False,
        str_to_upper=True
    )

    # Field constructor doesn't have parameters equivalent to str_strip_whitespace or str_to_upper
    first_name: Annotated[str, Field(min_length=1, max_length=255)]
    last_name: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, min_length=1, max_length=255)]

m1 = Model(first_name="       David \t\n", last_name="  \n\tJin  ")
print(repr(m1))    
    