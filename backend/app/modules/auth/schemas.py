from pydantic import BaseModel
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

class SessionRead(BaseModel):
    session_id: str
    expires_at: datetime