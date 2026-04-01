from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: str   # we can include product details in response
    product_price: float
    product_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime