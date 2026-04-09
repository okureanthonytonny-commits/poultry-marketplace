from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List

class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_snapshot: float
    product_name: Optional[str] = None
    product_image_url: Optional[str] = None

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemRead] = []

    @field_validator('status')
    def validate_status(cls, v):
        allowed = {'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'}
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v

class OrderStatusUpdate(BaseModel):
    status: str

    @field_validator('status')
    def validate_status(cls, v):
        allowed = {'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'}
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v