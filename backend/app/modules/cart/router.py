from fastapi import APIRouter, Depends, HTTPException, Query, logger
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.products.models import Product
from .services import add_to_cart, get_cart_items, update_cart_item, remove_cart_item, clear_cart
from .schemas import CartItemCreate, CartItemUpdate, CartItemRead

router = APIRouter(prefix="/cart", tags=["cart"])

def _load_products_by_ids(db: Session, product_ids: list[int], include_deleted: bool = False) -> dict[int, Product]:
    if not product_ids:
        return {}
    stmt = select(Product).where(Product.id.in_(product_ids))
    if not include_deleted:
        stmt = stmt.where(Product.deleted_at.is_(None))
    products = db.exec(stmt).all()
    return {product.id: product for product in products}

@router.get("/", response_model=list[CartItemRead])
def get_user_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    cart_items = get_cart_items(db, current_user.id)
    product_ids = [item.product_id for item in cart_items]
    product_map = _load_products_by_ids(db, product_ids, include_deleted=False)

    enriched = []
    for item in cart_items:
        product = product_map.get(item.product_id)
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
            logger.warning(f"Product not found for cart item: {item.id}")
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
    product = _load_products_by_ids(db, [cart_item.product_id], include_deleted=False).get(cart_item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found after add")
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

@router.put("/items/{product_id}", response_model=CartItemRead)
def update_item(
    product_id: int,
    update: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    item = update_cart_item(db, current_user.id, product_id, update.quantity)
    product = _load_products_by_ids(db, [item.product_id], include_deleted=False).get(item.product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Product no longer available")
    return {
        "id": item.id,
        "product_id": item.product_id,
        "quantity": item.quantity,
        "product_name": product.name,
        "product_price": product.price,
        "product_image_url": product.image_url,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }

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
    return None