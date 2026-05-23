import json
import os
from models import Dog

DB_FILE = os.getenv("DB_FILE", "dogs.json")


def load_dogs() -> list[Dog]:
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Dog(**item) for item in data]


def save_dogs(dogs: list[Dog]) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump([d.model_dump(mode="json") for d in dogs], f, ensure_ascii=False, indent=2)


def next_id(dogs: list[Dog]) -> int:
    return max((d.id for d in dogs), default=0) + 1
