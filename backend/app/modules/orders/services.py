from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime, timezone
from .models import Order, OrderItem
from app.modules.cart.services import get_cart_items, clear_cart
from app.modules.products.services import get_product
from app.modules.auth.models import User

def _validate_and_prepare_order_items(db: Session, cart_items: list) -> list:
    """Validate stock and prepare order items data."""
    order_items_data = []
    for cart_item in cart_items:
        product = get_product(db, cart_item.product_id, include_deleted=False)
        if not product:
            raise HTTPException(400, f"Product {cart_item.product_id} not available")
        if product.stock < cart_item.quantity:
            raise HTTPException(400, f"Insufficient stock for product {product.name}")
        order_items_data.append({
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "price_snapshot": product.price,
        })
        # Decrement stock immediately
        product.stock -= cart_item.quantity
        db.add(product)
    return order_items_data

def _create_order_record(db: Session, user_id: int) -> Order:
    order = Order(user_id=user_id, status="pending")
    db.add(order)
    db.flush()
    return order

def _create_order_items(db: Session, order_id: int, order_items_data: list):
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order_id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            price_snapshot=item_data["price_snapshot"],
        )
        db.add(order_item)

def create_order_from_cart(db: Session, user_id: int) -> Order:
    cart_items = get_cart_items(db, user_id)
    if not cart_items:
        raise HTTPException(400, "Cart is empty")

    try:
        order_items_data = _validate_and_prepare_order_items(db, cart_items)
        order = _create_order_record(db, user_id)
        _create_order_items(db, order.id, order_items_data)
        clear_cart(db, user_id)  # no commit inside
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise e

def get_user_orders(db: Session, user_id: int) -> list[Order]:
    stmt = select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
    return db.exec(stmt).all()

def get_order(db: Session, order_id: int, user_id: int, is_admin: bool = False) -> Order | None:
    stmt = select(Order).where(Order.id == order_id)
    if not is_admin:
        stmt = stmt.where(Order.user_id == user_id)
    return db.exec(stmt).first()

def update_order_status(db: Session, order_id: int, new_status: str) -> Order | None:
    order = db.get(Order, order_id)
    if not order:
        return None

    allowed_transitions = {
        "pending": ["confirmed", "cancelled"],
        "confirmed": ["shipped", "cancelled"],
        "shipped": ["delivered", "cancelled"],
        "delivered": [],
        "cancelled": [],
    }

    if new_status not in allowed_transitions.get(order.status, []):
        raise HTTPException(status_code=400, detail=f"Invalid transition from {order.status} to {new_status}")

    order.status = new_status
    order.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order