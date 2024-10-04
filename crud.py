import models
import schemas
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

def get_breeds(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Breed).offset(skip).limit(limit).all()

def create_breed(db: Session, breed: schemas.BreedCreate):
    db_breed = models.Breed(name=breed.name, description=breed.description)
    db.add(db_breed)
    db.commit()
    db.refresh(db_breed)
    return db_breed

def get_kittens(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Kitten).offset(skip).limit(limit).all()

def create_kittens(db: Session, kittens: list[schemas.KittenCreate]):
    try:
        created_kittens = []
        for kitten in kittens:
            # Проверка, существует ли порода с данным breed_id
            breed = db.query(models.Breed).filter(models.Breed.id == kitten.breed_id).first()
            if not breed:
                raise HTTPException(status_code=400, detail=f"Breed with id {kitten.breed_id} does not exist")

            # Создание котенка, если порода существует
            db_kitten = models.Kitten(
                name=kitten.name,
                color=kitten.color,
                age=kitten.age,
                description=kitten.description,
                breed_id=kitten.breed_id,
            )
            db.add(db_kitten)
            created_kittens.append(db_kitten)

        # Сохранение изменений в базе данных
        db.commit()

        # Обновляем данные каждого созданного котенка после сохранения
        for kitten in created_kittens:
            db.refresh(kitten)

        return created_kittens
    except SQLAlchemyError as e:
        db.rollback()  # Откатываем все изменения, если произошла ошибка
        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")

def get_kitten(db: Session, kitten_id: int):
    return db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()

def delete_kitten(db: Session, kitten_id: int):
    db_kitten = db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()
    db.delete(db_kitten)
    db.commit()

def get_kittens_by_breed(db: Session, breed_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Kitten).filter(models.Kitten.breed_id == breed_id).offset(skip).limit(limit).all()

def update_kitten(db: Session, kitten_id: int, kitten: schemas.KittenCreate):
    db_kitten = db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()
    if db_kitten is None:
        return None
    db_kitten.name = kitten.name
    db_kitten.color = kitten.color
    db_kitten.age = kitten.age
    db_kitten.description = kitten.description
    db_kitten.breed_id = kitten.breed_id
    db.commit()
    db.refresh(db_kitten)
    return db_kitten