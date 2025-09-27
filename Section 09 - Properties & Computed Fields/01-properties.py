import math

from functools import cached_property
from pydantic import BaseModel, Field

class Circle(BaseModel):
    center: tuple[float, float] = (0, 0)
    radius: float = Field(default=1, gt=0, frozen=True)

    @cached_property
    def area(self):
        print("Calculating area...")
        return round(math.pi * self.radius**2, 2)
    

c1 = Circle()
print(repr(c1))
print(c1.area)
print(c1.area)
print(c1.area)
print(c1.model_dump_json(indent=2))