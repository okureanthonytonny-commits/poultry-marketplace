#!/bin/bash

# Test authenticated endpoints with a valid session cookie
# Replace SESSION_ID with your actual cookie value

SESSION_ID="eJoiIRxjWYG2F4sASGRjI1BkcMCK8ZUm-LKJsxxOMlo"
BASE_URL="http://localhost:8000"

echo "=== Limelight v2 - Authenticated API Tests ==="
echo "Using session ID: ${SESSION_ID:0:20}..."

# Helper function
curl_auth() {
    curl -s -b "session_id=$SESSION_ID" "$@"
}

# 1. Auth: Get current user
echo -e "\n1. GET /auth/me"
curl_auth -X GET "$BASE_URL/auth/me" | jq .

# 2. Cart: Get cart (should have items)
echo -e "\n2. GET /cart/"
curl_auth -X GET "$BASE_URL/cart/" | jq .

# 3. Cart: Add item (if needed)
echo -e "\n3. POST /cart/items (add product 1, quantity 2)"
curl_auth -X POST "$BASE_URL/cart/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}' | jq .

# 4. Cart: Update item quantity
echo -e "\n4. PUT /cart/items/1 (set quantity to 5)"
curl_auth -X PUT "$BASE_URL/cart/items/1" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}' | jq .

# 5. Cart: Remove item
echo -e "\n5. DELETE /cart/items/1"
curl_auth -X DELETE "$BASE_URL/cart/items/1"

# 6. Cart: Clear cart
echo -e "\n6. DELETE /cart/"
curl_auth -X DELETE "$BASE_URL/cart/"

# 7. Orders: Create order from cart (cart should be empty or we add items first)
echo -e "\n7. POST /orders/ (create order)"
# First add an item to cart
curl_auth -X POST "$BASE_URL/cart/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}' > /dev/null
curl_auth -X POST "$BASE_URL/orders/" | jq .

# 8. Orders: List user orders
echo -e "\n8. GET /orders/"
curl_auth -X GET "$BASE_URL/orders/" | jq .

# 9. Orders: Get order detail (assuming order id=1)
echo -e "\n9. GET /orders/1"
curl_auth -X GET "$BASE_URL/orders/1" | jq .

# 10. Admin: Update order status (requires admin role)
echo -e "\n10. PATCH /orders/1/status (set to confirmed) - admin only"
curl_auth -X PATCH "$BASE_URL/orders/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmed"}' | jq .

echo -e "\n=== Tests completed ==="
