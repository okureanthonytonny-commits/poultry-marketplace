from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.modules.auth.models import User
from .services import get_cart, add_to_cart, update_cart_item, remove_cart_item, clear_cart
from .schemas import CartItemCreate, CartItemUpdate, CartItemRead

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=list[CartItemRead])
def get_user_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return get_cart(db, current_user.id)

@router.post("/items", response_model=CartItemRead, status_code=201)
def add_item(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return add_to_cart(db, current_user.id, item.product_id, item.quantity)

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
    return item

@router.delete("/items/{product_id}", status_code=204)
def remove_item(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    remove_cart_item(db, current_user.id, product_id)

@router.delete("/", status_code=204)
def clear(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    clear_cart(db, current_user.id)