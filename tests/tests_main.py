# test_main.py
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
print(sys.path)
from app.main import app, get_db
from app.database import Base
from app.models import Courier


# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений переменных окружения из .env файла
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")


# Создаем новую базу данных для тестов
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создаем движок базы данных
engine = create_engine(DATABASE_URL)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для получения базы данных в запросах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_get_available_courier():
    # Создаем курьера с доступным районом
    response = client.post(
        "/couriers/",
        json={"name": "Test Courier", "districts": ["District1"], "active_order": None}
    )
    assert response.status_code == 200
    data = response.json()
    courier_id = data["id"]

    # Проверяем, что курьер доступен
    response = client.get("/couriers/available/", params={"district": "District1"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == courier_id

    # Создаем заказ с районом, соответствующим курьеру
    response = client.post(
        "/orders/",
        json={"name": "Test Order", "district": "District1"}
    )
    assert response.status_code == 200
    data = response.json()
    order_id = data["id"]

    # Проверяем, что курьеру был присвоен заказ
    response = client.get(f"/couriers/{courier_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["active_order"] == order_id

    # Проверяем, что курьер больше не доступен
    response = client.get("/couriers/available/", params={"district": "District1"})
    assert response.status_code == 404