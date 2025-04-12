import uvicorn
from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from schemas import load_db, save_db, CarInput, CarOutput

app = FastAPI()
db = load_db()


# optional parameter to get call
@app.get("/api/cars")
async def get_cars(size: Optional[str] = None, doors: Optional[int] = None):
    if size:
        return [car for car in db if car.size == size]
    if doors:
        return [car for car in db if car.doors >= doors]

    return db


# path query - fastapi takes from path of url

@app.get("/api/cars/{id}")
def get_car_by_id(id: int):
    car_result = [car for car in db if car.id == id]
    if not car_result:
        raise HTTPException(status_code=404, detail=f"Car with ID {id} not found.")
    return car_result[0]


@app.post("/api/cars/")
def add_car(car: CarInput):
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id=len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car


@app.put("/api/cars/{id}")
def update_car_info(id: int, new_data: CarInput):
    car_to_update = [car for car in db if car.id == id]
    if car_to_update:
        res = car_to_update[0]
        res.fuel = new_data.fuel
        res.size = new_data.size
        res.doors = new_data.doors
        res.transmission = new_data.transmission
        save_db(db)
        return res
    else:
        raise HTTPException(status_code=404, details=f"No car with id={id}")


@app.delete("/api/cars/{id}", status_code=204)
def delete_car_record(id: int):
    car_to_del = [car for car in db if car.id == id]
    if car_to_del:
        results = car_to_del[0]
        db.remove(results)
        save_db(db)
    else:
        raise HTTPException(status_code=404, details=f"No car with id={id}")


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
