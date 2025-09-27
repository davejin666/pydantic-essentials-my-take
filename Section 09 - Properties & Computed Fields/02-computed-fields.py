import math

from functools import cached_property
from pydantic import BaseModel, computed_field, Field, ConfigDict

class Circle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    center: tuple[float, float] = (0, 0)
    radius: float = Field(default=1, gt=0, frozen=True)

    @computed_field(alias="circle_area", repr=True)
    @cached_property
    def area(self) -> float:
        print("Calculating area...")
        return round(math.pi * self.radius**2, 3)
    
c1 = Circle(center=(2, 2))
print(repr(c1))
print(Circle.model_fields)
print(c1.model_dump(by_alias=True))