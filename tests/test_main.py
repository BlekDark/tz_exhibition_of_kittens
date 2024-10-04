import pytest
from fastapi.testclient import TestClient
from main import app
from database import engine
from models import Base

# Создаем тестовый клиент
client = TestClient(app)


# Создание базы данных для тестов
@pytest.fixture(autouse=True)
def setup_database():
    # Создание всех таблиц
    Base.metadata.create_all(bind=engine)
    yield
    # Удаление всех таблиц после тестов
    Base.metadata.drop_all(bind=engine)


def test_get_breeds():
    # Создаем тестовые данные
    response = client.post("/breeds/",
                           json=[
                               {
                                   "name": "Сиамская",
                                   "description": "Добрая"
                               }
                           ]
                           )
    assert response.status_code == 200
    response = client.get("/breeds/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Сиамская"


def test_get_kittens():
    # Сначала добавим породу
    breed_response = client.post("/breeds/",
                                 json=[
                                     {
                                         "name": "Сиамска",
                                         "description": "Добрая"
                                     }
                                 ]
                                 )
    breed_id = breed_response.json()[0]["id"]

    # Добавляем котенка
    response = client.post("/kittens/",
                           json=[
                               {
                                   "name": "Мурка",
                                   "color": "серая",
                                   "age": 4,
                                   "description": "Красивая",
                                   "breed_id": 1
                               }
                           ]
                           )
    assert response.status_code == 200

    # Проверяем список всех котят
    response = client.get("/kittens/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_kitten():
    # Создаем породу
    breed_response = client.post("/breeds/",
                                 json=[
                                     {
                                         "name": "Сиамска",
                                         "description": "Добрая"
                                     }
                                 ]
                                 )
    breed_id = breed_response.json()[0]["id"]

    # Добавляем котенка
    response = client.post("/kittens/",
                           json=[
                               {
                                   "name": "Котенок 2",
                                   "color": "черный",
                                   "age": 6,
                                   "description": "Игривый",
                                   "breed_id": 1
                               }
                           ]
    )
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Котенок 2"


def test_create_multiple_kittens():
    # Создаем породу
    breed_response = client.post("/breeds/",
                                 json=[
                                     {
                                         "name": "Сиамска",
                                         "description": "Добрая"
                                     }
                                 ]
                                 )
    breed_id = breed_response.json()[0]["id"]

    # Добавляем несколько котят
    response = client.post("/kittens/", json=[
        {
            "name": "Котенок 3",
            "color": "белый",
            "age": 4,
            "description": "Игривый котенок",
            "breed_id": breed_id
        },
        {
            "name": "Котенок 4",
            "color": "рыжий",
            "age": 2,
            "description": "Смешной котенок",
            "breed_id": breed_id
        }
    ])
    assert response.status_code == 200
    assert len(response.json()) == 2


