# Set up model relationships after all models are defined
# This is needed to avoid circular import issues

from sqlmodel import Relationship
from app.modules.products.models import Product
from app.modules.cart.models import CartItem
from app.modules.auth.models import User

# Add relationships - must be done after all classes are defined
Product.cart_items = Relationship(back_populates="product")  # type: ignore
CartItem.user = Relationship(back_populates="cart_items")    # type: ignore
CartItem.product = Relationship(back_populates="cart_items") # type: ignore
User.cart_items = Relationship(back_populates="user")        # type: ignore
