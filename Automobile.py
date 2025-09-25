from datetime import date
from enum import Enum
from uuid import uuid4, UUID
from typing import Annotated, TypeVar
from pprint import pprint
from pydantic import (
    BaseModel, 
    ConfigDict, 
    Field, 
    field_serializer, 
    FieldSerializationInfo, 
    UUID4, 
    StringConstraints, 
    ValidationError
)
from pydantic.alias_generators import to_camel

class AutomobileType(Enum):
    sedan = "Sedan"
    coupe = "Coupe"
    convertible = "Convertible"
    suv = "SUV"
    truck = "Truck"

def make_alias(field_name: str):
    alias = to_camel(field_name)
    return alias.removesuffix("_")

BoundedString = Annotated[str, StringConstraints(min_length=2, max_length=50)]

ElementType = TypeVar("ElementType")
BoundedList = Annotated[list[ElementType], Field(min_length=1, max_length=5)]

class Automobile(BaseModel):
    model_config = ConfigDict(
        extra="forbid", 
        str_strip_whitespace=True,
        validate_assignment=True,
        validate_default=True,
        alias_generator=make_alias
    )

    # id_: UUID4 | None = Field(default_factory=uuid4)
    id_: UUID4 = Field(default_factory=uuid4)
    manufacturer: BoundedString
    series_name: BoundedString
    type_: AutomobileType
    is_electric: bool = False
    manufactured_date: date = Field(validation_alias="completionDate", ge=date(1980, 1, 1))
    base_msrp_usd: float = Field(validation_alias="msrpUSD", serialization_alias="baseMSRPUSD")
    top_features: BoundedList[BoundedString] | None = None
    vin: BoundedString
    number_of_doors: int = Field(default=4, validation_alias="doors", ge=2, le=4, multiple_of=2)
    registration_country: BoundedString | None = None
    license_plate: BoundedString | None = None

    @field_serializer("manufactured_date", when_used="unless-none")
    def date_serializer(self, date: date, info: FieldSerializationInfo):
        if info.mode_is_json():
            return date.strftime("%Y/%m/%d")
        return date

# Deserializing and serializing
data = {
    "id": "c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7",
    "manufacturer": "BMW",
    "seriesName": "M4 Competition xDrive",
    "type": "Convertible",
    "isElectric": False,
    "completionDate": "2023-01-01",
    "msrpUSD": 93_300,
    "topFeatures": ["6 cylinders", "all-wheel drive", "convertible"],
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB"
}

expected_serialized_by_alias = {
    'id': UUID('c4e60f4a-3c7f-4da5-9b3f-07aee50b23e7'),
    'manufacturer': 'BMW',
    'seriesName': 'M4 Competition xDrive',
    'type': AutomobileType.convertible,
    'isElectric': False,
    'manufacturedDate': date(2023, 1, 1),
    'baseMSRPUSD': 93300.0,
    'topFeatures': ['6 cylinders', 'all-wheel drive', 'convertible'],
    'vin': '1234567890',
    'numberOfDoors': 2,
    'registrationCountry': 'France',
    'licensePlate': 'AAA-BBB'
}

a1 = Automobile.model_validate(data)
print(a1.model_dump(by_alias=True) == expected_serialized_by_alias)