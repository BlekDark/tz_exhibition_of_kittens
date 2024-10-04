from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kitten Online Exhibition API",
    description="API for managing kitten online exhibition, including breed and kitten data management.",
    version="1.0.0",
)

# Dependency для создания сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/breeds/", response_model=list[schemas.Breed])
def read_breeds(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
        Получить список всех пород котят.

        Параметры:
        - **skip**: пропустить N элементов (по умолчанию 0).
        - **limit**: ограничить количество результатов (по умолчанию 10).
        """
    breeds = crud.get_breeds(db, skip=skip, limit=limit)
    return breeds

@app.post("/breeds/", response_model=list[schemas.Breed], description="Добавить одну или несколько пород котят")
def create_breeds(breeds: list[schemas.BreedCreate], db: Session = Depends(get_db)):
    """
    Добавить одну или несколько пород котят.

    Требуется передать список объектов, каждый из которых содержит:
    - **name**: название породы.
    - **description**: описание породы.
    """
    created_breeds = [crud.create_breed(db, breed) for breed in breeds]
    return created_breeds

@app.get("/kittens/", response_model=list[schemas.Kitten])
def read_kittens(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
        Получить список всех котят.

        Параметры:
        - **skip**: пропустить N элементов (по умолчанию 0).
        - **limit**: ограничить количество результатов (по умолчанию 10).
        """
    return crud.get_kittens(db, skip=skip, limit=limit)

@app.post("/kittens/", response_model=list[schemas.Kitten], description="Добавить одного или нескольких котят")
def create_kittens_endpoint(kittens: list[schemas.KittenCreate], db: Session = Depends(get_db)):
    """
    Добавить одного или нескольких котят.

    Требуется передать список объектов, каждый из которых содержит:
    - **name**: имя котенка.
    - **color**: цвет котенка.
    - **age**: возраст котенка (не более 24 месяцев).
    - **description**: описание котенка.
    - **breed_id**: ID породы котенка.
    """
    # Вызов CRUD-функции для создания котят
    created_kittens = crud.create_kittens(db, kittens)
    return created_kittens

@app.get("/kittens/{kitten_id}", response_model=schemas.Kitten)
def read_kitten(kitten_id: int, db: Session = Depends(get_db)):
    """
        Получить подробную информацию о котенке по его ID.

        Параметры:
        - **kitten_id**: ID котенка.
        """
    db_kitten = crud.get_kitten(db, kitten_id=kitten_id)
    if db_kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return db_kitten

@app.delete("/kittens/{kitten_id}")
def delete_kitten(kitten_id: int, db: Session = Depends(get_db)):
    """
        Удалить котенка по его ID.

        Параметры:
        - **kitten_id**: ID котенка.
        """
    crud.delete_kitten(db, kitten_id)
    return {"message": "Kitten deleted"}

@app.get("/kittens/breed/{breed_id}", response_model=list[schemas.Kitten], description="Получить список котят по породе")
def read_kittens_by_breed(breed_id: int, db: Session = Depends(get_db)):
    """
    Получить список котят по ID породы.

    Параметры:
    - **breed_id**: ID породы котенка.
    """
    kittens = crud.get_kittens_by_breed(db, breed_id=breed_id)
    return kittens

@app.put("/kittens/{kitten_id}", response_model=schemas.Kitten, description="Изменить информацию о котенке")
def update_kitten(kitten_id: int, kitten: schemas.KittenCreate, db: Session = Depends(get_db)):
    """
    Обновить информацию о котенке.

    Параметры:
    - **kitten_id**: ID котенка.
    - Передайте обновленные данные для котенка.
    """
    updated_kitten = crud.update_kitten(db, kitten_id=kitten_id, kitten=kitten)
    if updated_kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return updated_kitten
