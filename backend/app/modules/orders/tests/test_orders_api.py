import pytest
from app.modules.products.models import Product
from app.modules.cart.models import CartItem

def test_create_order_workflow(auth_client, session, test_user):
    # 1. Seed a product
    product = Product(name="Test Item", price=10.0, stock=5)
    session.add(product)
    session.commit()

    # 2. Add to cart
    cart_item = CartItem(user_id=test_user.id, product_id=product.id, quantity=2)
    session.add(cart_item)
    session.commit()

    # 3. Place Order
    response = auth_client.post("/orders/")
    assert response.status_code == 201
    
    # 4. Assertions on the side effects
    data = response.json()
    assert data["status"] == "pending"
    
    # Check stock was decremented (5 - 2 = 3)
    session.refresh(product)
    assert product.stock == 3
    
    # Check cart was cleared
    response_cart = auth_client.get("/cart/")
    assert len(response_cart.json()) == 0

def test_list_orders(auth_client, session, test_user):
    # Seed dummy order
    from app.modules.orders.models import Order
    session.add(Order(user_id=test_user.id, status="pending"))
    session.commit()

    response = auth_client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_admin_update_order_status(admin_client, session, test_user):
    from app.modules.orders.models import Order
    order = Order(user_id=test_user.id, status="pending")
    session.add(order)
    session.commit()
    session.refresh(order)

    response = admin_client.patch(f"/orders/{order.id}/status", json={"status": "confirmed"})
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"