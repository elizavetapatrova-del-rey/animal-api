from fastapi import FastAPI, HTTPException, Header, Query, Depends
from typing import Optional
import json
import os

from models import Dog, DogCreate, Gender
from storage import load_dogs, save_dogs, next_id

SECRET_TOKEN = os.getenv("SHELTER_TOKEN", "supersecret")

app = FastAPI(
    title="Animal Shelter API",
    description="API для управления собачками в приюте",
    version="1.0.0",
)


def verify_token(x_secret_token: str = Header(...)):
    """Dependency: проверяет секретный токен из заголовка X-Secret-Token."""
    if x_secret_token != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid secret token")


@app.get("/dogs", response_model=list[Dog], summary="Список собачек")
def get_dogs(
    available: Optional[bool] = Query(None, description="True — только в приюте"),
    gender: Optional[Gender] = Query(None, description="male / female"),
    breed: Optional[str] = Query(None, description="Фильтр по породе"),
    age: Optional[int] = Query(None, description="Фильтр по возрасту (полных лет)"),
):
    """
    Возвращает список собачек с опциональными фильтрами:
    - **available** — только те, кто ещё в приюте
    - **gender** — пол (male / female)
    - **breed** — порода (регистронезависимо)
    - **age** — точный возраст
    """
    dogs = load_dogs()

    if available is not None:
        dogs = [d for d in dogs if d.is_available == available]
    if gender is not None:
        dogs = [d for d in dogs if d.gender == gender]
    if breed is not None:
        dogs = [d for d in dogs if d.breed.lower() == breed.lower()]
    if age is not None:
        dogs = [d for d in dogs if d.age == age]

    return dogs


@app.get("/dogs/{dog_id}", response_model=Dog, summary="Собачка по ID")
def get_dog(dog_id: int):
    """Возвращает одну собачку по ID. Если не найдена — 404."""
    dogs = load_dogs()
    for dog in dogs:
        if dog.id == dog_id:
            return dog
    raise HTTPException(status_code=404, detail=f"Dog with id={dog_id} not found")


@app.post(
    "/dogs",
    response_model=Dog,
    status_code=201,
    summary="Добавить собачку",
    dependencies=[Depends(verify_token)],
)
def create_dog(dog_data: DogCreate):
    """
    Добавляет новую собачку. Требует заголовок **X-Secret-Token**.
    """
    dogs = load_dogs()
    new_dog = Dog(id=next_id(dogs), **dog_data.model_dump())
    dogs.append(new_dog)
    save_dogs(dogs)
    return new_dog
