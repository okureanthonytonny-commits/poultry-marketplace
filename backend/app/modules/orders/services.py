from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime, timezone
from .models import Order, OrderItem
from app.modules.cart.services import get_cart_items, clear_cart
from app.modules.products.services import get_product

def _validate_cart_items(db: Session, cart_items: list) -> list[tuple]:
    """Validate the cart items and return pairs of (cart_item, product)."""
    validated = []
    for cart_item in cart_items:
        product = get_product(db, cart_item.product_id, include_deleted=False)
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {cart_item.product_id} not available")
        if product.stock < cart_item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
        validated.append((cart_item, product))
    return validated


def _build_order_items_data(validated_items: list[tuple]) -> list[dict]:
    """Build order item payloads from validated cart/product pairs."""
    return [
        {
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "price_snapshot": product.price,
        }
        for cart_item, product in validated_items
    ]


def _decrement_stock(db: Session, validated_items: list[tuple]) -> None:
    """Apply stock decrement to validated products."""
    for cart_item, product in validated_items:
        product.stock -= cart_item.quantity
        db.add(product)

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
        raise HTTPException(status_code=400, detail="Cart is empty")

    try:
        validated_items = _validate_cart_items(db, cart_items)
        order_items_data = _build_order_items_data(validated_items)
        _decrement_stock(db, validated_items)
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

def cancel_order(db: Session, user_id: int, order_id: int) -> Order | None:
    order = get_order(db, order_id, user_id, is_admin=False)
    if not order:
        return None
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")
    
    try:
        order_items_stmt = select(OrderItem).where(OrderItem.order_id == order.id)
        order_items = db.exec(order_items_stmt).all()
        for item in order_items:
            product = get_product(db, item.product_id, include_deleted=False)
            if product:
                product.stock += item.quantity
                db.add(product)
        order.status = "cancelled"
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        raise e