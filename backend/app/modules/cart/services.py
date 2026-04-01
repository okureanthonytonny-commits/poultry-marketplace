from sqlmodel import Session, select
from .models import CartItem
from app.modules.products.models import Product
from app.modules.products.services import get_product  # reuse
from fastapi import HTTPException

def get_cart(db: Session, user_id: int):
    stmt = select(CartItem).where(CartItem.user_id == user_id)
    items = db.exec(stmt).all()
    # Enrich with product details
    enriched = []
    for item in items:
        product = get_product(db, item.product_id, include_deleted=False)
        if product:
            enriched.append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_name": product.name,
                "product_price": product.price,
                "product_image_url": product.image_url,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            })
        else:
            # If product is deleted, remove from cart automatically
            db.delete(item)
    db.commit()
    return enriched

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    # Check product exists and is not deleted
    product = get_product(db, product_id, include_deleted=False)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Check if item already in cart
    stmt = select(CartItem).where(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    )
    existing = db.exec(stmt).first()
    if existing:
        existing.quantity += quantity
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

def update_cart_item(db: Session, user_id: int, product_id: int, quantity: int):
    stmt = select(CartItem).where(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    )
    item = db.exec(stmt).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    if quantity <= 0:
        db.delete(item)
        db.commit()
        return None
    else:
        # Check product stock
        product = get_product(db, product_id, include_deleted=False)
        if not product:
            raise HTTPException(status_code=400, detail="Product no longer available")
        if product.stock < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        item.quantity = quantity
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

def remove_cart_item(db: Session, user_id: int, product_id: int):
    stmt = select(CartItem).where(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    )
    item = db.exec(stmt).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    db.delete(item)
    db.commit()

def clear_cart(db: Session, user_id: int):
    stmt = select(CartItem).where(CartItem.user_id == user_id)
    items = db.exec(stmt).all()
    for item in items:
        db.delete(item)
    db.commit()