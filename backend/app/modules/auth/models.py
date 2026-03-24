from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
from enum import Enum

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    role: UserRole = Field(default=UserRole.CUSTOMER)
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

class Session(SQLModel, table=True):
    __tablename__ = "sessions"
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(default_factory=lambda: secrets.token_urlsafe(32), unique=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    expires_at: datetime = Field(default_factory=lambda: (datetime.now(timezone.utc) + timedelta(days=7)).replace(tzinfo=None))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))