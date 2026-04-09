from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.cart.models import CartItem
from app.modules.products.services import get_product
from .services import add_to_cart, get_cart_items, update_cart_item, remove_cart_item, clear_cart
from .schemas import CartItemCreate, CartItemUpdate, CartItemRead

router = APIRouter(prefix="/cart", tags=["cart"])

def _enrich_cart_item(cart_item: CartItem, db: Session) -> dict | None:
    product = get_product(db, cart_item.product_id, include_deleted=False)
    if not product:
        return None
    return {
        "id": cart_item.id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "product_name": product.name,
        "product_price": product.price,
        "product_image_url": product.image_url,
        "created_at": cart_item.created_at,
        "updated_at": cart_item.updated_at,
    }

@router.get("/", response_model=list[CartItemRead])
def get_user_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    cart_items = get_cart_items(db, current_user.id)
    enriched = []
    for item in cart_items:
        enriched_item = _enrich_cart_item(item, db)
        if enriched_item:
            enriched.append(enriched_item)
        else:
            # Product missing – remove item from cart
            db.delete(item)
    db.commit()
    return enriched

@router.post("/items", response_model=CartItemRead, status_code=201)
def add_item(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    cart_item = add_to_cart(db, current_user.id, item.product_id, item.quantity)
    enriched = _enrich_cart_item(cart_item, db)
    if not enriched:
        raise HTTPException(status_code=404, detail="Product not found after add")
    return enriched

@router.put("/items/{product_id}", response_model=CartItemRead)
def update_item(
    product_id: int,
    update: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    item = update_cart_item(db, current_user.id, product_id, update.quantity)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not in cart")
    enriched = _enrich_cart_item(item, db)
    if not enriched:
        raise HTTPException(status_code=400, detail="Product no longer available")
    return enriched

@router.delete("/items/{product_id}", status_code=204)
def remove_item_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    remove_cart_item(db, current_user.id, product_id)

@router.delete("/", status_code=204)
def clear_user_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    clear_cart(db, current_user.id)
    db.commit()
    return None