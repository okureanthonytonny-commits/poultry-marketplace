from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.core.dependencies import get_current_user, require_admin
from app.modules.auth.models import User
from app.modules.orders.models import Order, OrderItem
from .services import create_order_from_cart, get_user_orders, get_order, update_order_status
from .schemas import OrderRead, OrderStatusUpdate
from app.modules.products.services import get_product
from sqlmodel import select
from app.modules.products.services import get_product

def _enrich_order(order: Order, db: Session) -> dict:
    # Load order items
    stmt = select(OrderItem).where(OrderItem.order_id == order.id)
    items = db.exec(stmt).all()
    enriched_items = []
    for item in items:
        product = get_product(db, item.product_id, include_deleted=True)
        enriched_items.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price_snapshot": item.price_snapshot,
            "product_name": product.name if product else "Deleted Product",
            "product_image_url": product.image_url if product else None,
        })
    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "items": enriched_items,
    }

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead, status_code=201)
def create_order(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    order = create_order_from_cart(db, current_user.id)
    return _enrich_order(order, db)

@router.get("/", response_model=list[OrderRead])
def list_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    orders = get_user_orders(db, current_user.id)
    # Enrich each order with items (we'll do in a separate helper)
    # For simplicity, we'll add enrichment in a separate function
    return [_enrich_order(order, db) for order in orders]

@router.get("/{order_id}", response_model=OrderRead)
def get_order_detail(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    is_admin = current_user.role == "admin"
    order = get_order(db, order_id, current_user.id, is_admin=is_admin)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _enrich_order(order, db)

@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status_endpoint(
    order_id: int,
    status_update: OrderStatusUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_session)
):
    order = update_order_status(db, order_id, status_update.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _enrich_order(order, db)