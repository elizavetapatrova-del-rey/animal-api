from pydantic import BaseModel, Field
from enum import Enum
from datetime import date
from typing import Optional


class Gender(str, Enum):
    male = "male"
    female = "female"


class DogCreate(BaseModel):
    name: str = Field(..., examples=["Шарик"])
    breed: str = Field(..., examples=["Дворняга"])
    age: int = Field(..., ge=0, le=30, examples=[3])
    gender: Gender
    arrived_at: date = Field(..., description="Дата появления в приюте")
    is_available: bool = Field(True, description="True — собачка ещё в приюте")

    model_config = {"json_schema_extra": {
        "example": {
            "name": "Шарик",
            "breed": "Дворняга",
            "age": 3,
            "gender": "male",
            "arrived_at": "2024-06-01",
            "is_available": True,
        }
    }}


class Dog(DogCreate):
    id: int
