Animal Shelter API

FastAPI-сервис для управления собачками в приюте.

Структура файлов



shelter/
├── main.py          # Роутеры и логика эндпоинтов
├── models.py        # Pydantic-модели
├── storage.py       # Чтение/запись JSON-файла
├── requirements.txt
└── dogs.json        # БД


REST API — декомпозиция

| Метод  | URL           | Авторизация | Описание                              |
|--------|---------------|-------------|---------------------------------------|
| GET    | `/dogs`       | —           | Список всех собачек (с фильтрами)     |
| GET    | `/dogs/{id}`  | —           | Одна собачка по ID                    |
| POST   | `/dogs`       | Токен       | Добавить новую собачку                |

Query-параметры GET /dogs

| Параметр    | Тип     | Описание                              |
|-------------|---------|---------------------------------------|
| `available` | bool    | `true` — только те, кто в приюте      |
| `gender`    | string  | `male` / `female`                     |
| `breed`     | string  | Порода (регистронезависимо)           |
| `age`       | integer | Точный возраст в годах                |

Запуск

pip install -r requirements.txt

Запуск (токен по умолчанию: supersecret)
uvicorn main:app --reload

Или с кастомным токеном и файлом БД
SHELTER_TOKEN=mytoken DB_FILE=/var/data/dogs.json uvicorn main:app --reload


Примеры запросов

Все собачки в приюте, женского пола
curl "http://localhost:8000/dogs?available=true&gender=female"

Добавить собачку (нужен токен)
curl -X POST http://localhost:8000/dogs \
  -H "Content-Type: application/json" \
  -H "X-Secret-Token: supersecret" \
  -d '{
    "name": "Шарик",
    "breed": "Дворняга",
    "age": 3,
    "gender": "male",
    "arrived_at": "2024-06-01",
    "is_available": true
  }'

Получить собачку по ID
curl http://localhost:8000/dogs/1

Swagger UI
open http://localhost:8000/docs
