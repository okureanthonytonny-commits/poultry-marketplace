import pytest
from app.modules.products.models import Product

def test_get_empty_cart(auth_client):
    response = auth_client.get("/cart/")
    assert response.status_code == 200
    assert response.json() == []

def test_add_to_cart(auth_client, session):
    product = Product(name="Cart Item", price=15.0, stock=10)
    session.add(product)
    session.commit()
    session.refresh(product)

    response = auth_client.post("/cart/items", json={"product_id": product.id, "quantity": 2})
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == product.id
    assert data["quantity"] == 2

def test_update_cart_quantity(auth_client, session):
    product = Product(name="Update Item", price=15.0, stock=10)
    session.add(product)
    session.commit()
    session.refresh(product)

    auth_client.post("/cart/items", json={"product_id": product.id, "quantity": 1})
    response = auth_client.put(f"/cart/items/{product.id}", json={"quantity": 5})
    assert response.status_code == 200
    assert response.json()["quantity"] == 5

def test_remove_item_from_cart(auth_client, session):
    product = Product(name="Remove Item", price=15.0, stock=10)
    session.add(product)
    session.commit()
    session.refresh(product)

    auth_client.post("/cart/items", json={"product_id": product.id, "quantity": 1})
    response = auth_client.delete(f"/cart/items/{product.id}")
    assert response.status_code == 204
    assert auth_client.get("/cart/").json() == []

def test_clear_cart(auth_client, session):
    p1 = Product(name="P1", price=10, stock=10)
    p2 = Product(name="P2", price=20, stock=10)
    session.add_all([p1, p2])
    session.commit()

    auth_client.post("/cart/items", json={"product_id": p1.id, "quantity": 1})
    auth_client.post("/cart/items", json={"product_id": p2.id, "quantity": 1})
    
    response = auth_client.delete("/cart/")
    assert response.status_code == 204
    assert auth_client.get("/cart/").json() == []

def test_add_exceeding_stock(auth_client, session):
    product = Product(name="Low Stock", price=10, stock=2)
    session.add(product)
    session.commit()
    response = auth_client.post("/cart/items", json={"product_id": product.id, "quantity": 5})
    assert response.status_code == 400