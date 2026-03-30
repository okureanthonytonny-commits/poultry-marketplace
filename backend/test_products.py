import requests

BASE_URL = "http://localhost:8000"
SESSION_ID = "UKqPjYx3prGe6LMFcvw62alY-dKzVHwCkD46wY9Xsbk"  # replace with actual value

headers = {"Cookie": f"session_id={SESSION_ID}"}

def test_products():
    # Create product (admin only)
    product_data = {"name": "Test Product", "price": 19.99, "stock": 10}
    resp = requests.post(f"{BASE_URL}/api/products/", json=product_data, headers=headers)
    print("Create product:", resp.status_code, resp.json())
    if resp.status_code != 201:
        return
    product = resp.json()
    product_id = product["id"]

    # List public products (should contain our product)
    resp = requests.get(f"{BASE_URL}/api/products/")
    print("Public list before delete:", [p["name"] for p in resp.json()])

    # Soft delete product (admin)
    resp = requests.delete(f"{BASE_URL}/api/products/admin/{product_id}?hard=false", headers=headers)
    print("Soft delete:", resp.status_code)

    # List public products (should not contain our product)
    resp = requests.get(f"{BASE_URL}/api/products/")
    print("Public list after delete:", [p["name"] for p in resp.json()])

    # Restore product (admin)
    resp = requests.post(f"{BASE_URL}/api/products/admin/{product_id}/restore", headers=headers)
    print("Restore:", resp.status_code)

    # List public products (should contain our product again)
    resp = requests.get(f"{BASE_URL}/api/products/")
    print("Public list after restore:", [p["name"] for p in resp.json()])

if __name__ == "__main__":
    test_products()