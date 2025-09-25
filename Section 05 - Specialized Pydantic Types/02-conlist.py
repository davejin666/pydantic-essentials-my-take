from pydantic import BaseModel, conlist, PositiveFloat, ValidationError

class Sphere(BaseModel):
    center: conlist(int, min_length=2, max_length=3) = [0, 0]
    radius: PositiveFloat = 1

s1 = Sphere(center=[1, 2, 3])
print(repr(s1))
s2 = Sphere(center=[2, 3])
print(repr(s2))

try:
    Sphere(center=[1, 2, 3, 4])
except ValidationError as exc:
    print(exc)