from pydantic import BaseModel
from datetime import datetime

class ItemCreate(BaseModel):
    name: str

class ItemRead(BaseModel):
    id: int
    name: str
    created_at: datetime
