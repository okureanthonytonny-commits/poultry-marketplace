from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional


class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    product_id: int = Field(foreign_key="products.id", nullable=False)
    quantity: int = Field(default=1, ge=1)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc).replace(tzinfo=None)}
    )