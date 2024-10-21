from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

str_100 = Annotated[str, Field(max_length=100)]


class CategoryCreate(BaseModel):
    title: str_100


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str_100


class CategoryUpdate(BaseModel):
    title: Optional[str_100] = None


class ProductCreate(BaseModel):
    title: str_100
    description: str
    price: float
    category_id: int


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str_100
    description: str
    price: float
    category: Category


class ProductUpdate(BaseModel):
    title: Optional[str_100] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
