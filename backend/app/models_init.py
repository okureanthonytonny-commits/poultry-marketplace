"""
Model initialization - sets up relationships after all models are defined.
This module must be imported after all models are loaded.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.products.models import Product
    from app.modules.cart.models import CartItem
    from app.modules.auth.models import User


def init_relationships():
    """Initialize relationships between models after import."""
    from sqlmodel import Relationship
    from app.modules.products.models import Product
    from app.modules.cart.models import CartItem
    from app.modules.auth.models import User
    
    # Set relationships on Product
    Product.cart_items = Relationship(back_populates="product")  # type: ignore
    
    # Set relationships on CartItem
    CartItem.user = Relationship(back_populates="cart_items")    # type: ignore
    CartItem.product = Relationship(back_populates="cart_items")  # type: ignore
    
    # Set relationships on User
    User.cart_items = Relationship(back_populates="user")        # type: ignore
