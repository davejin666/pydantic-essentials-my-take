from datetime import date, timezone
from enum import Enum
from pprint import pprint
from pydantic import BaseModel, ConfigDict, Field, field_serializer, FieldSerializationInfo
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

class Automobile(BaseModel):
    model_config = ConfigDict(
        extra="forbid", 
        str_strip_whitespace=True,
        validate_assignment=True,
        validate_default=True,
        alias_generator=make_alias
    )

    manufacturer: str
    series_name: str
    type_: AutomobileType
    is_electric: bool = False
    manufactured_date: date = Field(validation_alias="completionDate")
    base_msrp_usd: float = Field(validation_alias="msrpUSD", serialization_alias="baseMSRPUSD")
    vin: str
    number_of_doors: int = Field(default=4, validation_alias="doors")
    registration_country: str | None = None
    license_plate: str | None = None

    @field_serializer("manufactured_date", when_used="unless-none")
    def date_serializer(self, date: date, info: FieldSerializationInfo):
        if info.mode_is_json():
            return date.strftime("%Y/%m/%d")
        return date

# Deserializing and serializing
data_json = '''
{
    "manufacturer": "BMW",
    "seriesName": "M4",
    "type": "Convertible",
    "isElectric": false,
    "completionDate": "2023-01-01",
    "msrpUSD": 93300,
    "vin": "1234567890",
    "doors": 2,
    "registrationCountry": "France",
    "licensePlate": "AAA-BBB"
}
'''

expected_serialized_dict = {
    'manufacturer': 'BMW',
    'series_name': 'M4',
    'type_': AutomobileType.convertible,
    'is_electric': False,
    'manufactured_date': date(2023, 1, 1),
    'base_msrp_usd': 93300.0,
    'vin': '1234567890',
    'number_of_doors': 2,
    'registration_country': 'France',
    'license_plate': 'AAA-BBB'
}

expected_serialized_dict_by_alias = {
    'manufacturer': 'BMW',
    'seriesName': 'M4',
    'type': AutomobileType.convertible,
    'isElectric': False,
    'manufacturedDate': date(2023, 1, 1),
    'baseMSRPUSD': 93300.0,
    'vin': '1234567890',
    'numberOfDoors': 2,
    'registrationCountry': 'France',
    'licensePlate': 'AAA-BBB'
}

expected_serialized_json_by_alias = (
    '{"manufacturer":"BMW","seriesName":"M4","type":"Convertible",'
    '"isElectric":false,"manufacturedDate":"2023/01/01","baseMSRPUSD":93300.0,'
    '"vin":"1234567890","numberOfDoors":2,"registrationCountry":"France",'
    '"licensePlate":"AAA-BBB"}'
)

a1 = Automobile.model_validate_json(data_json)

print(a1.model_dump() == expected_serialized_dict)
print(a1.model_dump(by_alias=True) == expected_serialized_dict_by_alias)
print(a1.model_dump_json(by_alias=True) == expected_serialized_json_by_alias)