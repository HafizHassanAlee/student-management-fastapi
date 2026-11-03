from pydantic import BaseModel, Field


class Student(BaseModel):
    name:str
    age:int
    roll_no:int
    department:str
    email:str

class Product(BaseModel):

    name: str = Field(min_length=3, max_length=50)

    price: int = Field(gt=0)

    quantity: int = Field(gt=0)

    discount: int = Field(ge=0, lt=100)
