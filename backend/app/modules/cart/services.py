from typing import List
from sqlmodel import Session, delete, select
from .models import CartItem
from app.modules.products.services import get_product  # reuse
from app.core.errors import ConflictError, InsufficientStockError, NotFoundError, ValidationError

def _validate_product_availability(db: Session, product_id: int, quantity: int):
    product = get_product(db, product_id, include_deleted=False)
    if not product:
        raise NotFoundError("Product not found")
    if product.stock < quantity:
        raise InsufficientStockError("Insufficient stock")
    return product

def get_cart_items(db: Session, user_id: int) -> List[CartItem] | None:
    stmt = select(CartItem).where(CartItem.user_id == user_id)
    result = db.exec(stmt).all()
    return result if result else None

def get_cart_item(db: Session, user_id: int, product_id: int) -> CartItem | None:
    stmt = select(CartItem).where(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    )
    return db.exec(stmt).first()

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int) -> CartItem:
    if quantity < 1:
        raise ValidationError("Quantity must be positive")

    _validate_product_availability(db, product_id, quantity)
    existing = get_cart_item(db, user_id, product_id)
    if existing:
        raise ConflictError("Item already in cart")

    cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int) -> CartItem:


    #_validate_product_availability(db, product_id, quantity)
    item = get_cart_item(db, user_id, product_id)
    if not item:
        raise NotFoundError("Item not in cart")

    item.quantity = quantity
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_cart_item(db: Session, user_id: int, product_id: int) -> bool:
    item = get_cart_item(db, user_id, product_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

def clear_cart(db: Session, user_id: int) -> int:
    stmt = delete(CartItem).where(CartItem.user_id == user_id)
    result = db.exec(stmt)
    db.commit()
    return result.rowcount
