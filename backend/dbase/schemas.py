from typing import List, Optional
from pydantic import BaseModel, Field
import enum


class CategoryEnum(enum.Enum):
    TSHIRT = "tshirts"
    SOCKS = "socks"


class UserRegistration(BaseModel):
    username: str = Field(min_length=4, max_length=12, pattern=r'^[a-zA-Z][a-zA-Z0-9]*$')
    password: str = Field(min_length=4, max_length=12)


class ProductCreate(BaseModel):
    name: str
    price: float
    size: Optional[str] = None
    quantity: int
    category: CategoryEnum


class ProductUpdate(BaseModel):
    name: str
    price: float
    size: Optional[str] = None
    main_image: str
    quantity: int
    category: CategoryEnum

