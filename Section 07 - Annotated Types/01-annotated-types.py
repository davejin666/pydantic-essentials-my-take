from datetime import datetime, UTC
from typing import Annotated, get_args
from pydantic import Field

AfterBirth = Annotated[datetime | None, Field(ge=datetime(1988, 7, 16, 2, 10)), "abc", [1, 2, 3]]

print(get_args(AfterBirth))
