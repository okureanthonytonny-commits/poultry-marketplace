from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.core.database import get_session
from app.core.dependencies import get_current_user, require_admin
from app.modules.auth.models import User
from .services import create_product, get_product, list_products, update_product, delete_product, restore_product
from .schemas import ProductCreate, ProductUpdate, ProductRead, ProductReadPublic

router = APIRouter(prefix="/products", tags=["products"])

# Public endpoints (no auth, only non‑deleted)
@router.get("/", response_model=list[ProductReadPublic])
def public_list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_session)
):
    return list_products(db, skip=skip, limit=limit, include_deleted=False)

@router.get("/{product_id}", response_model=ProductReadPublic)
def public_get_product(product_id: int, db: Session = Depends(get_session)):
    product = get_product(db, product_id, include_deleted=False)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Admin endpoints (require admin role)
@router.post("/", response_model=ProductRead, status_code=201)
def admin_create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_session),
    _: User = Depends(require_admin)
):
    return create_product(db, product_data)

@router.get("/admin/all", response_model=list[ProductRead])
def admin_list_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    include_deleted: bool = False,
    db: Session = Depends(get_session),
    _: User = Depends(require_admin)
):
    return list_products(db, skip=skip, limit=limit, include_deleted=include_deleted)

@router.get("/admin/{product_id}", response_model=ProductRead)
def admin_get_product(
    product_id: int,
    include_deleted: bool = False,
    db: Session = Depends(get_session),
    _: User = Depends(require_admin)
):
    product = get_product(db, product_id, include_deleted=include_deleted)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/admin/{product_id}", response_model=ProductRead)
def admin_update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_session),
    _: User = Depends(require_admin)
):
    product = update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/admin/{product_id}", status_code=204)
def admin_delete_product(
    product_id: int,
    hard: bool = False,
    db: Session = Depends(get_session),
    _: User = Depends(require_admin)
):
    if not delete_product(db, product_id, hard=hard):
        raise HTTPException(status_code=404, detail="Product not found")
    return None

@router.post("/admin/{product_id}/restore", response_model=ProductRead)
def admin_restore_product(
    product_id: int,
    db: Session = Depends(get_session),
    _: User = Depends(require_admin)
):
    product = restore_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not deleted")
    return product