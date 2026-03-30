from datetime import datetime, timezone

from sqlmodel import Session, select
from .models import Product
from .schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException

def create_product(db: Session, product_data: ProductCreate) -> Product:
    # Optional: prevent duplicate names (case‑insensitive, ignoring soft‑deleted)
    existing = db.exec(
        select(Product).where(Product.name == product_data.name, Product.deleted_at.is_(None))
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Product with this name already exists")
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int, include_deleted: bool = False) -> Product | None:
    query = select(Product).where(Product.id == product_id)
    if not include_deleted:
        query = query.where(Product.deleted_at.is_(None))
    return db.exec(query).first()

def list_products(db: Session, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> list[Product]:
    query = select(Product)
    if not include_deleted:
        query = query.where(Product.deleted_at.is_(None))
    return db.exec(query.offset(skip).limit(limit)).all()

def update_product(db: Session, product_id: int, update_data: ProductUpdate) -> Product | None:
    product = get_product(db, product_id, include_deleted=True)  # allow updating deleted? maybe not
    if not product:
        return None
    # If name is being changed, check for duplicate (excluding current product)
    if update_data.name is not None and update_data.name != product.name:
        existing = db.exec(
            select(Product).where(
                Product.name == update_data.name,
                Product.deleted_at.is_(None),
                Product.id != product_id
            )
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Another product with this name already exists")
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int, hard: bool = False) -> bool:
    product = get_product(db, product_id, include_deleted=True)
    if not product:
        return False
    if hard:
        db.delete(product)
    else:
        product.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.add(product)
    db.commit()
    return True

def restore_product(db: Session, product_id: int) -> Product | None:
    product = db.get(Product, product_id)
    if product and product.deleted_at is not None:
        product.deleted_at = None
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    return None