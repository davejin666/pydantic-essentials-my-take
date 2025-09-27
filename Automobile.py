from datetime import date
from enum import Enum
from uuid import uuid4, UUID
from typing import Annotated, TypeVar, Any
from functools import cached_property
from pydantic import (
    BaseModel, 
    ConfigDict, 
    Field, 
    field_serializer, 
    FieldSerializationInfo, 
    field_validator,
    ValidationInfo,
    UUID4, 
    StringConstraints, 
    ValidationError,
    BeforeValidator,
    AfterValidator,
    computed_field
)
from pydantic.alias_generators import to_camel
from dateutil import parser

class AutomobileType(Enum):
    sedan = "Sedan"
    coupe = "Coupe"
    convertible = "Convertible"
    suv = "SUV"
    truck = "Truck"

countries = {
    "australia": ("Australia", "AUS"),
    "canada": ("Canada", "CAN"),
    "china": ("China", "CHN"),
    "france": ("France", "FRA"),
    "germany": ("Germany", "DEU"),
    "india": ("India", "IND"),
    "mexico": ("Mexico", "MEX"),
    "norway": ("Norway", "NOR"),
    "pakistan": ("Pakistan", "PAK"),
    "san marino": ("San Marino", "SMR"),
    "sanmarino": ("San Marino", "SMR"),
    "spain": ("Spain", "ESP"),
    "sweden": ("Sweden", "SWE"),
    "united kingdom": ("United Kingdom", "GBR"),
    "uk": ("United Kingdom", "GBR"),
    "great britain": ("United Kingdom", "GBR"),
    "britain": ("United Kingdom", "GBR"),
    "us": ("United States of America", "USA"),
    "united states": ("United States of America", "USA"),
    "usa": ("United States of America", "USA"),
}

country_codes = {
    name: code
    for name, code
    in countries.values()
}

def make_alias(field_name: str):
    alias = to_camel(field_name)
    return alias.removesuffix("_")

def parse_dt_str(value: Any):
    if isinstance(value, str):
        try:
            parsed_date = parser.parse(value).date()
        except Exception as exc:
            raise ValueError(str(exc))
        else:
            return parsed_date
    return value

    
def validate_country_name(name: str):
    name_lower = name.lower()

    if name_lower in countries:
        return countries[name_lower][0]
    raise ValueError(f"Invalid country name: {name}")

BoundedString = Annotated[str, StringConstraints(min_length=2, max_length=50)]

ElementType = TypeVar("ElementType")
BoundedList = Annotated[list[ElementType], Field(min_length=1, max_length=5)]

ValidDate = Annotated[date, BeforeValidator(parse_dt_str)]
ValidCountry = Annotated[str, AfterValidator(validate_country_name)]

class Automobile(BaseModel):
    model_config = ConfigDict(
        extra="forbid", 
        str_strip_whitespace=True,
        validate_assignment=True,
        validate_default=True,
        alias_generator=make_alias,
    )

    # id_: UUID4 | None = Field(default_factory=uuid4)
    id_: UUID4 = Field(default_factory=uuid4)
    manufacturer: BoundedString
    series_name: BoundedString
    type_: AutomobileType
    is_electric: bool = Field(default=False, repr=False)
    manufactured_date: date = Field(validation_alias="completionDate", ge=date(1980, 1, 1))
    base_msrp_usd: float = Field(validation_alias="msrpUSD", serialization_alias="baseMSRPUSD", repr=False)
    top_features: BoundedList[BoundedString] | None = Field(default=None, repr=False)
    vin: BoundedString = Field(repr=False)
    number_of_doors: int = Field(default=4, validation_alias="doors", ge=2, le=4, multiple_of=2)
    registration_country: ValidCountry | None = Field(default=None, frozen=True)
    registration_date: date | None = None
    license_plate: BoundedString | None = None

    @field_serializer("manufactured_date", "registration_date", when_used="unless-none")
    def date_serializer(self, date: date, info: FieldSerializationInfo):
        if info.mode_is_json():
            return date.strftime("%Y/%m/%d")
        return date
    
    @field_validator("registration_date", mode="after")
    @classmethod
    def registration_after_manfactured(cls, d: date | None, info: ValidationInfo):
        if isinstance(d, date) and ("manufactured_date" in info.data):
            if d < info.data["manufactured_date"]:
                raise ValueError(f'`registration_date` must be preceded by `manufactured_date`.')
        return d
    
    @computed_field(alias="registrationCountryCode")
    @cached_property
    def registration_country_code(self) -> str:
        return country_codes.get(self.registration_country, None)

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
    "registrationCountry": "us",
    "registrationDate": "2023-06-01",
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
    'registrationCountry': 'United States of America',
    'registrationCountryCode': 'USA',
    'registrationDate': date(2023, 6, 1),
    'licensePlate': 'AAA-BBB',
}

try:
    a1 = Automobile.model_validate(data)
except ValidationError as exc:
    print(exc.json(indent=2))
else:
    print(repr(a1))