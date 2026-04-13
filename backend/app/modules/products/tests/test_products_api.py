import pytest
from app.modules.products.models import Product

def test_list_products_empty(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_product_admin(admin_client):
    payload = {
        "name": "Test Widget",
        "description": "High quality widget",
        "price": 49.99,
        "stock": 100
    }
    response = admin_client.post("/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Widget"

def test_create_product_customer_forbidden(auth_client):
    payload = {"name": "Hacker Product", "price": 0.01}
    response = auth_client.post("/products/", json=payload)
    assert response.status_code == 403

def test_get_product_detail(client, session):
    product = Product(name="Detail Item", price=10.0, stock=5)
    session.add(product)
    session.commit()
    session.refresh(product)

    response = client.get(f"/products/{product.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Detail Item"

def test_update_product_admin(admin_client, session):
    product = Product(name="Old Name", price=10.0, stock=5)
    session.add(product)
    session.commit()
    session.refresh(product)

    response = admin_client.put(f"/products/admin/{product.id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"

def test_delete_product_admin(admin_client, session):
    product = Product(name="To Delete", price=10.0, stock=5)
    session.add(product)
    session.commit()
    session.refresh(product)

    response = admin_client.delete(f"/products/admin/{product.id}")
    assert response.status_code == 204
    
    # Verify it is not in public list
    assert admin_client.get("/products/").json() == []