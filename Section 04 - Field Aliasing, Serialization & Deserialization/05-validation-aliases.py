from pydantic import BaseModel, AliasChoices, ConfigDict, Field
from pprint import pprint

data = {
    "databases": {
        "redis": {
            "name": "Local Redis",
            "redis_conn": "redis://secret@localhost:9000/1"
        },
        "pgsql": {
            "name": "Local Postgres",
            "pgsql_conn": "postgresql://user:secret@localhost"
        },
        "nosql": {
            "name": "Local MongoDB",
            "mongo_conn": "mongodb://USERNAME:PASSWORD@HOST/DATABASE"
        }
    }
}

class DB(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    name: str
    connection: str = Field(validation_alias=AliasChoices("redis_conn", "pgsql_conn", "mongo_conn"))

dbs = {}

for k, v in data["databases"].items():
    dbs[k] = DB.model_validate(v).model_dump_json(indent=2)

pprint(dbs)