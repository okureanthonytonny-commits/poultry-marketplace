import requests
import json

BASE_URL = "http://localhost:8000"

# Preferably set via environment variable: export SESSION_ID="your_cookie_here"
SESSION_ID = "eJoiIRxjWYG2F4sASGRjI1BkcMCK8ZUm-LKJsxxOMlo"

# Headers with session cookie
headers = {"Cookie": f"session_id={SESSION_ID}"}

def test_public_endpoints():
    print("\n📦 Testing Public Product Endpoints")
    # List products
    resp = requests.get(f"{BASE_URL}/products/")
    print(f"GET /products/ -> {resp.status_code}")
    if resp.status_code == 200:
        products = resp.json()
        print(f"  Found {len(products)} products")
        if products:
            first_id = products[0]["id"]
            # Get single product
            resp2 = requests.get(f"{BASE_URL}/products/{first_id}")
            print(f"GET /products/{first_id} -> {resp2.status_code}")
    else:
        print("  Failed to fetch products")

def test_cart_operations():
    print("\n🛒 Testing Cart Endpoints (Authenticated)")
    # Get cart (should be empty initially)
    resp = requests.get(f"{BASE_URL}/cart/", headers=headers)
    print(f"GET /cart/ -> {resp.status_code}")
    if resp.status_code == 401:
        print("  Authentication failed – check session cookie")
        return False
    if resp.status_code == 200:
        cart = resp.json()
        print(f"  Cart has {len(cart)} items")
    else:
        print("  Unexpected response")
        return False

    # Add an item (product_id=1)
    add_data = {"product_id": 1, "quantity": 2}
    resp = requests.post(f"{BASE_URL}/cart/items", json=add_data, headers=headers)
    print(f"POST /cart/items -> {resp.status_code}")
    if resp.status_code == 201:
        item = resp.json()
        print(f"  Added product {item['product_id']} quantity {item['quantity']}")
    elif resp.status_code == 400:
        print(f"  Error: {resp.json().get('detail')}")
    else:
        print("  Failed to add item")
        return False

    # Get cart again
    resp = requests.get(f"{BASE_URL}/cart/", headers=headers)
    cart = resp.json()
    print(f"GET /cart/ -> {len(cart)} items")

    # Update quantity of the added item
    update_data = {"quantity": 5}
    resp = requests.put(f"{BASE_URL}/cart/items/1", json=update_data, headers=headers)
    print(f"PUT /cart/items/1 -> {resp.status_code}")
    if resp.status_code == 200:
        print(f"  Updated quantity to {resp.json()['quantity']}")

    # Remove item
    resp = requests.delete(f"{BASE_URL}/cart/items/1", headers=headers)
    print(f"DELETE /cart/items/1 -> {resp.status_code}")

    # Test invalid product ID
    print("  Testing invalid product ID...")
    resp = requests.get(f"{BASE_URL}/products/9999999", headers=headers)
    assert resp.status_code == 404, f"Expected 404 for invalid product, got {resp.status_code}"
    print("  ✅ Correctly handled invalid ID")

    # Test stock limit enforcement
    print("  Testing stock limit enforcement...")
    # Assuming product 1 has stock < 1000
    overstock_data = {"product_id": 1, "quantity": 1000}
    resp = requests.post(f"{BASE_URL}/cart/items", json=overstock_data, headers=headers)
    if resp.status_code in [400, 422]:
        print(f"  ✅ Correctly blocked overstock: {resp.json().get('detail')}")
    else:
        print(f"  ❌ Failed to block overstock: {resp.status_code}")

    # Clean up cart
    requests.delete(f"{BASE_URL}/cart/", headers=headers)
    print("  Cart cleaned up.")

    return True

def test_admin_product_ops():
    print("\n🔧 Testing Admin Product Endpoints (requires admin role)")
    # Create product
    product_data = {
        "name": "Integration Test Product",
        "price": 99.99,
        "stock": 50,
        "description": "Created by test script"
    }
    resp = requests.post(f"{BASE_URL}/products/", json=product_data, headers=headers)
    print(f"POST /products/ -> {resp.status_code}")
    if resp.status_code == 201:
        product = resp.json()
        product_id = product["id"]
        print(f"  Created product id={product_id}")

        # Update product
        update_data = {"price": 89.99}
        resp2 = requests.put(f"{BASE_URL}/products/admin/{product_id}", json=update_data, headers=headers)
        print(f"PUT /products/admin/{product_id} -> {resp2.status_code}")

        # Soft delete
        resp3 = requests.delete(f"{BASE_URL}/products/admin/{product_id}?hard=false", headers=headers)
        print(f"DELETE /products/admin/{product_id} (soft) -> {resp3.status_code}")

        # Restore
        resp4 = requests.post(f"{BASE_URL}/products/admin/{product_id}/restore", headers=headers)
        print(f"POST /products/admin/{product_id}/restore -> {resp4.status_code}")

        # Hard delete (optional – uncomment if needed)
        # resp5 = requests.delete(f"{BASE_URL}/products/admin/{product_id}?hard=true", headers=headers)
        # print(f"DELETE /products/admin/{product_id} (hard) -> {resp5.status_code}")

        return True
    elif resp.status_code == 403:
        print("  Admin role required – skipping admin tests")
        return False
    else:
        print(f"  Unexpected error: {resp.json()}")
        return False

if __name__ == "__main__":
    print("🔐 Make sure you have a valid session cookie")
    print(f"Using SESSION_ID: {SESSION_ID[:20]}...")
    test_public_endpoints()
    test_cart_operations()
    test_admin_product_ops()
    print("\n✅ Integration tests completed.")
