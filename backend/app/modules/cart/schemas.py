from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int

    @field_validator('quantity')
    def quantity_positive(cls, v):
        if v < 1:
            raise ValueError('Quantity must be at least 1')
        return v

class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str   # we can include product details in response
    product_price: float
    product_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime