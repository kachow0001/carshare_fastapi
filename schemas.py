import json
from typing import Optional
from pydantic import BaseModel


class CarInput(BaseModel):
    size: str
    fuel: Optional[str] = "hybrid"
    doors: int
    transmission: Optional[str] = "auto"


class CarOutput(CarInput):
    id: int


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
