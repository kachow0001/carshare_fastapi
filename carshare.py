import uvicorn
from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List

app = FastAPI()
db = [
    {"id": 1, "size": "s", "fuel": "gasoline", "doors": 3, "transmission": "auto"},
    {"id": 2, "size": "s", "fuel": "electric", "doors": 3, "transmission": "auto"},
    {"id": 3, "size": "s", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
    {"id": 4, "size": "m", "fuel": "electric", "doors": 3, "transmission": "auto"},
    {"id": 5, "size": "m", "fuel": "hybrid", "doors": 5, "transmission": "auto"},
    {"id": 6, "size": "m", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
    {"id": 7, "size": "l", "fuel": "diesel", "doors": 5, "transmission": "manual"},
    {"id": 8, "size": "l", "fuel": "electric", "doors": 5, "transmission": "auto"},
    {"id": 9, "size": "l", "fuel": "hybrid", "doors": 5, "transmission": "auto"}
]


# optional parameter to get call
@app.get("/api/cars")
async def get_cars(size: Optional[str] = None, doors: Optional[int] = None):
    if size:
        return [car for car in db if car['size'] == size]
    if doors:
        return [car for car in db if car['doors'] >= doors]

    return db


# path query - fastapi takes from path of url

@app.get("/api/cars/{id}")
def get_car_by_id(id: int):
    car_result = [car for car in db if car["id"] == id]
    if not car_result:
        raise HTTPException(status_code=404, detail=f"Car with ID {id} not found.")
    return car_result[0]


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
