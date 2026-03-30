import pytest
from datetime import datetime, timezone
from sqlmodel import create_engine, Session, SQLModel
from app.modules.products.models import Product
from app.modules.products.services import create_product, get_product, list_products, update_product, delete_product, restore_product
from app.modules.products.schemas import ProductCreate, ProductUpdate
from fastapi import HTTPException

@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db(engine):
    with Session(engine) as session:
        yield session

def test_create_product(db):
    data = ProductCreate(name="Test", price=10.0, stock=5)
    product = create_product(db, data)
    assert product.id is not None
    assert product.name == "Test"
    assert product.deleted_at is None

def test_create_duplicate_name(db):
    data = ProductCreate(name="Unique", price=10.0)
    create_product(db, data)
    with pytest.raises(HTTPException) as exc:
        create_product(db, data)
    assert exc.value.status_code == 409

def test_get_product(db):
    data = ProductCreate(name="GetTest", price=5.0)
    created = create_product(db, data)
    fetched = get_product(db, created.id)
    assert fetched is not None
    assert fetched.id == created.id

def test_list_products(db):
    data1 = ProductCreate(name="A", price=1)
    data2 = ProductCreate(name="B", price=2)
    create_product(db, data1)
    create_product(db, data2)
    products = list_products(db)
    assert len(products) == 2

def test_update_product(db):
    data = ProductCreate(name="Old", price=10)
    product = create_product(db, data)
    update = ProductUpdate(name="New", price=20)
    updated = update_product(db, product.id, update)
    assert updated.name == "New"
    assert updated.price == 20

def test_soft_delete_product(db):
    data = ProductCreate(name="ToDelete", price=100)
    product = create_product(db, data)
    assert delete_product(db, product.id, hard=False) == True
    # public query should not see it
    fetched = get_product(db, product.id, include_deleted=False)
    assert fetched is None
    # admin with include_deleted=True should see it
    fetched_admin = get_product(db, product.id, include_deleted=True)
    assert fetched_admin.deleted_at is not None

def test_restore_product(db):
    data = ProductCreate(name="RestoreMe", price=50)
    product = create_product(db, data)
    delete_product(db, product.id, hard=False)
    restored = restore_product(db, product.id)
    assert restored is not None
    assert restored.deleted_at is None
    # now public can see it again
    fetched = get_product(db, product.id)
    assert fetched is not None