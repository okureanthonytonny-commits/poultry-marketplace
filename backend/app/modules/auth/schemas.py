from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None
    oauth_provider: str
    oauth_id: str

class UserRead(BaseModel):
    id: int
    email: str
    name: Optional[str]
    role: str
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None

    @field_validator('role')
    def validate_role(cls, v):
        if v is not None and v not in ('customer', 'admin'):
            raise ValueError('Role must be "customer" or "admin"')
        return v    

class SessionRead(BaseModel):
    session_id: str
    expires_at: datetime