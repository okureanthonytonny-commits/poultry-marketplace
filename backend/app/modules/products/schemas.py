from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    image_url: Optional[str] = None

    @field_validator('price')
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

    @field_validator('stock')
    def stock_non_negative(cls, v):
        if v < 0:
            raise ValueError('Stock cannot be negative')
        return v

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None

    # validators similar, allowing None

class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]   # expose only to admin; for public we'll omit via separate schema

# For public lists, we can use ProductReadPublic that excludes deleted_at
class ProductReadPublic(ProductRead):
    deleted_at: None = None  # explicitly hidden