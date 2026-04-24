import requests
import json
import sys

BASE_URL = "http://localhost:8000"
#SESSION_ID = input("Enter session_id from browser (press Enter to skip auth tests): ").strip()
SESSION_ID = "iyvUhBQaBDuIskIsPm3yGisJuujkHXz8dP1gBxRVVs4"

headers = {"Content-Type": "application/json"}
if SESSION_ID:
    headers["Cookie"] = f"session_id={SESSION_ID}"

def log_response(title, resp):
    print(f"\n{title}:")
    print(f"  Status: {resp.status_code}")
    try:
        print(f"  Body: {json.dumps(resp.json(), indent=2)}")
    except:
        print(f"  Body: {resp.text}")

def safe_request(method, url, **kwargs):
    try:
        resp = requests.request(method, url, headers=headers, **kwargs)
        return resp
    except Exception as e:
        print(f"Request failed: {e}")
        return None

# Test 1: Public product list
resp = safe_request("GET", f"{BASE_URL}/products/")
log_response("GET /products/ (public)", resp)

# Test 2: Auth (if session provided)
if SESSION_ID:
    resp = safe_request("GET", f"{BASE_URL}/auth/me")
    log_response("GET /auth/me", resp)

# Test 3: Cart operations (requires session)
if SESSION_ID:
    # Clear cart first
    resp = safe_request("DELETE", f"{BASE_URL}/cart/")
    log_response("DELETE /cart/ (clear)", resp)

    # Add product 1, quantity 2
    resp = safe_request("POST", f"{BASE_URL}/cart/items", json={"product_id": 1, "quantity": 2})
    log_response("POST /cart/items (add 2)", resp)

    # Get cart
    resp = safe_request("GET", f"{BASE_URL}/cart/")
    log_response("GET /cart/", resp)

    # Update quantity to 5
    resp = safe_request("PUT", f"{BASE_URL}/cart/items/1", json={"quantity": 5})
    log_response("PUT /cart/items/1 (update to 5)", resp)

    # Remove item
    resp = safe_request("DELETE", f"{BASE_URL}/cart/items/1")
    log_response("DELETE /cart/items/1", resp)

    # Get cart (should be empty)
    resp = safe_request("GET", f"{BASE_URL}/cart/")
    log_response("GET /cart/ after remove", resp)

    # Clear cart again
    resp = safe_request("DELETE", f"{BASE_URL}/cart/")
    log_response("DELETE /cart/ (final clear)", resp)

    # Test order creation with empty cart (should fail)
    resp = safe_request("POST", f"{BASE_URL}/orders/")
    log_response("POST /orders/ (empty cart, expect 400)", resp)

print("\n✅ Test completed.")