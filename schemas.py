from pydantic import BaseModel, Field

class BreedBase(BaseModel):
    name: str
    description: str

class BreedCreate(BreedBase):
    pass

class Breed(BreedBase):
    id: int

    class Config:
        orm_mode = True

class KittenBase(BaseModel):
    name: str
    color: str
    age: int = Field(..., le=24, description="Возраст котенка не может быть больше 24 месяцев")
    description: str
    breed_id: int

    class Config:
        from_attributes = True


class KittenCreate(KittenBase):
    pass

class Kitten(KittenBase):
    id: int

    class Config:
        orm_mode = True
