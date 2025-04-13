import json
from typing import Optional
from pydantic import BaseModel


class TripsInput(BaseModel):
    start: int
    end: int
    description: str


class TripsOutput(TripsInput):
    id: int


class CarInput(BaseModel):
    size: str
    fuel: Optional[str] = "hybrid"
    doors: int
    transmission: Optional[str] = "auto"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "size": "m",
                    "doors": 4,
                    "transmission": "manual",
                    "fuel": "hybrid"
                }
            ]
        }
    }


class CarOutput(CarInput):
    id: int
    trips: list[TripsOutput] = []


def load_db():
    """
   loads list of car obj from json file
    :return:  list[dict]
    """
    with open("cars.json") as fp:
        return [CarOutput.model_validate(obj) for obj in json.load(fp)]


def save_db(cars: list[CarOutput]):
    with open("cars.json", "w") as fp:
        json.dump([car.model_dump() for car in cars], fp, indent=4)
