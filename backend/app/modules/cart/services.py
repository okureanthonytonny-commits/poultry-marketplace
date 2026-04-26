from typing import List
from sqlmodel import Session, select
from .models import CartItem
from app.modules.products.services import get_product  # reuse
from fastapi import HTTPException

def _validate_product_availability(db: Session, product_id: int, quantity: int):
        # Check product exists and is not deleted
    product = get_product(db, product_id, include_deleted=False)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    return product

def get_cart_items(db: Session, user_id: int) -> List[CartItem]:
    stmt = select(CartItem).where(CartItem.user_id == user_id)
    return db.exec(stmt).all()

def get_cart_item(db: Session, user_id: int, product_id: int) -> CartItem | None:
    stmt = select(CartItem).where(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    )
    return db.exec(stmt).first()

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int) -> CartItem:
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    _validate_product_availability(db, product_id, quantity)
    existing = get_cart_item(db, user_id, product_id)
    if existing:
        raise HTTPException(status_code=409, detail="Item already in cart")

    cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int) -> CartItem:
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    _validate_product_availability(db, product_id, quantity)
    item = get_cart_item(db, user_id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    item.quantity = quantity
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_cart_item(db: Session, user_id: int, product_id: int):
    item = get_cart_item(db, user_id, product_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    db.delete(item)
    db.commit()

def clear_cart(db: Session, user_id: int):
    items = get_cart_items(db, user_id)
    for item in items:
        db.delete(item)
    db.commit()
