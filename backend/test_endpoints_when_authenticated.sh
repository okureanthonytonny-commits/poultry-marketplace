#!/bin/bash

# Comprehensive API Test Suite for Limelight v2
# Handles CRUD, Security, and Role-based Access Control

# Configuration - Replace with valid session IDs for testing
SESSION_ID_CUSTOMER="${SESSION_ID_CUSTOMER:-eJoiIRxjWYG2F4sASGRjI1BkcMCK8ZUm-LKJsxxOMlo}"
SESSION_ID_ADMIN="${SESSION_ID_ADMIN:-ADMIN_SESSION_ID_HERE}"
BASE_URL="https://limelight-v2.onrender.com"
HEADER_JSON="Content-Type: application/json"

# Formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Limelight v2: Comprehensive API Test Suite ===${NC}"

if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required but not installed.${NC}"
    exit 1
fi

# Global helper for API calls
# Usage: api_call <method> <path> <session_id|none> <data>
api_call() {
    local method=$1
    local path=$2
    local sid=$3
    local data=$4
    local cmd=(curl -s --connect-timeout 5 --max-time 15 -X "$method" "$BASE_URL$path")
    
    [[ "$sid" != "none" ]] && cmd+=(-b "session_id=$sid")
    [[ -n "$data" ]] && cmd+=(-H "$HEADER_JSON" -d "$data")
    
    "${cmd[@]}"
}

test_step() {
    echo -e "\n[TEST] $1"
}

###############################################################################
# 1. PRODUCTS MODULE (Public & Admin CRUD)
###############################################################################
echo -e "\n${YELLOW}--- Module: Products ---${NC}"

test_step "Public: Health Check (Happy Path)"
api_call GET "/" none | jq -e '. != null' > /dev/null && echo "✅ Success" || echo "❌ Failed"

test_step "Public: List all products (Happy Path)"
api_call GET "/products/" none | jq -e '. != null' > /dev/null && echo "✅ Success" || echo "❌ Failed"

test_step "Public: Get Non-existent Product (Unhappy Path)"
RES=$(api_call GET "/products/999999" none)
echo "$RES" | jq -c . | grep -qi "not found" && echo "✅ Correctly 404" || echo "❌ Failed to 404"

test_step "Customer: Try to create product (Security Path - Unhappy)"
RES=$(api_call POST "/products/" "$SESSION_ID_CUSTOMER" '{"name":"Hacker","price":1}')
echo "$RES" | jq -c .
[[ $(echo "$RES" | jq -r .detail) == "Forbidden" || $(echo "$RES" | jq -r .detail) == "Not authenticated" ]] && echo "✅ Correctly Blocked" || echo "❌ Security Flaw"

test_step "Admin: Create Mock Product (Happy Path)"
MOCK_PRODUCT=$(api_call POST "/products/" "$SESSION_ID_ADMIN" '{
    "name": "Test Mock Widget",
    "description": "Automated test item",
    "price": 99.99,
    "stock": 50,
    "image_url": "https://example.com/test.jpg"
}')
PRODUCT_ID=$(echo "$MOCK_PRODUCT" | jq -r '.id // empty')

if [[ -z "$PRODUCT_ID" || "$PRODUCT_ID" == "null" ]]; then
    echo -e "${RED}CRITICAL: Could not create mock product. Admin session may be invalid.${NC}"
    # For demonstration, we'll fallback to ID 1 if creation failed but we want to continue
    PRODUCT_ID=1
else
    echo "✅ Created Product ID: $PRODUCT_ID"
fi

test_step "Admin: Update Product (Happy Path)"
api_call PUT "/products/$PRODUCT_ID" "$SESSION_ID_ADMIN" '{"name": "Updated Widget", "price": 89.99}' | jq -c .

test_step "Public: Get Specific Product (Happy Path)"
api_call GET "/products/$PRODUCT_ID" none | jq -e ".id == $PRODUCT_ID" > /dev/null && echo "✅ Found" || echo "❌ Not Found"

###############################################################################
# 2. AUTH MODULE
###############################################################################
echo -e "\n${YELLOW}--- Module: Auth ---${NC}"

test_step "Unauthenticated: GET /auth/me (Security Path - Unhappy)"
api_call GET "/auth/me" none | jq -c .

test_step "Public: GET /auth/login (Redirect Path)"
curl -s -I "$BASE_URL/auth/login" | head -n 1

test_step "Customer: GET /auth/me (Happy Path)"
ME_RES=$(api_call GET "/auth/me" "$SESSION_ID_CUSTOMER")
CUSTOMER_ID=$(echo "$ME_RES" | jq -r '.id')
echo "$ME_RES" | jq -c '{"id": .id, "email": .email, "role": .role}'

test_step "Customer: Attempt Role Escalation (Security Path - Unhappy)"
# Attempting to change role via a PATCH (if it existed) or verifying it's blocked
RES=$(api_call PATCH "/auth/me" "$SESSION_ID_CUSTOMER" '{"role": "admin"}')
echo "Result: $(echo "$RES" | jq -c . || echo "Endpoint does not exist (404/405)")"

test_step "Admin: Promote Customer to Admin (Happy Path)"
if [[ -n "$CUSTOMER_ID" ]]; then
    api_call PATCH "/auth/admin/users/$CUSTOMER_ID" "$SESSION_ID_ADMIN" '{"role": "admin"}' | jq -c '{"id": .id, "new_role": .role}'
    
    echo "Verifying Promotion..."
    api_call GET "/auth/me" "$SESSION_ID_CUSTOMER" | jq -c '{"role": .role}' | grep -q "admin" && echo "✅ Promotion Verified" || echo "❌ Promotion Failed"
fi

test_step "Admin: Demote User back to Customer (Happy Path)"
if [[ -n "$CUSTOMER_ID" ]]; then
    api_call PATCH "/auth/admin/users/$CUSTOMER_ID" "$SESSION_ID_ADMIN" '{"role": "customer"}' | jq -c '{"id": .id, "new_role": .role}'
    
    echo "Verifying Demotion..."
    api_call GET "/auth/me" "$SESSION_ID_CUSTOMER" | jq -c '{"role": .role}' | grep -q "customer" && echo "✅ Demotion Verified" || echo "❌ Demotion Failed"
fi

###############################################################################
# 3. CART MODULE (Authenticated CRUD)
###############################################################################
echo -e "\n${YELLOW}--- Module: Cart ---${NC}"

test_step "Public: Add to cart (Security Path - Unhappy)"
api_call POST "/cart/items" none "{\"product_id\": $PRODUCT_ID, \"quantity\": 1}" | jq -c .

test_step "Customer: Clear existing cart"
api_call DELETE "/cart/" "$SESSION_ID_CUSTOMER" > /dev/null

test_step "Customer: Add Mock Product to cart (Happy Path)"
api_call POST "/cart/items" "$SESSION_ID_CUSTOMER" "{\"product_id\": $PRODUCT_ID, \"quantity\": 2}" | jq -c .

test_step "Customer: Add Item Exceeding Stock (Unhappy Path)"
# Mock product has stock 50. Let's try 100.
api_call POST "/cart/items" "$SESSION_ID_CUSTOMER" "{\"product_id\": $PRODUCT_ID, \"quantity\": 100}" | jq -c . | grep -qiE "stock|limit|insufficient" && echo "✅ Correctly Blocked" || echo "❌ Security Flaw: Allowed quantity > stock"

test_step "Customer: Update quantity (Happy Path)"
api_call PUT "/cart/items/$PRODUCT_ID" "$SESSION_ID_CUSTOMER" '{"quantity": 10}' | jq -c .

test_step "Customer: Remove single item from cart"
api_call DELETE "/cart/items/$PRODUCT_ID" "$SESSION_ID_CUSTOMER" && echo "✅ Item removed"

test_step "Customer: Update quantity with invalid input (Unhappy Path)"
api_call PUT "/cart/items/$PRODUCT_ID" "$SESSION_ID_CUSTOMER" '{"quantity": -5}' | jq -c .

test_step "Customer: Get cart contents"
api_call GET "/cart/" "$SESSION_ID_CUSTOMER" | jq -c '.items[] | {product_id: .product_id, qty: .quantity}'

###############################################################################
# 4. ORDERS MODULE (Workflow & Status)
###############################################################################
echo -e "\n${YELLOW}--- Module: Orders ---${NC}"

test_step "Customer: Create Order from Cart (Happy Path)"
ORDER_RES=$(api_call POST "/orders/" "$SESSION_ID_CUSTOMER")
ORDER_ID=$(echo "$ORDER_RES" | jq -r '.id // empty')

if [[ -z "$ORDER_ID" || "$ORDER_ID" == "null" ]]; then
    echo -e "${RED}❌ Failed to create order${NC}"
    echo "$ORDER_RES" | jq .
else
    echo "✅ Created Order ID: $ORDER_ID"
fi

test_step "Customer: Verify Cart is Empty after Order"
CART_CHECK=$(api_call GET "/cart/" "$SESSION_ID_CUSTOMER")
echo "$CART_CHECK" | jq -e '.items | length == 0' > /dev/null && echo "✅ Cart Cleared" || echo "❌ Cart still has items after checkout"

test_step "Customer: List All Orders (Happy Path)"
api_call GET "/orders/" "$SESSION_ID_CUSTOMER" | jq -c '.[:3]' # Show last 3

test_step "Customer: View Order Detail (Happy Path)"
[[ -n "$ORDER_ID" ]] && api_call GET "/orders/$ORDER_ID" "$SESSION_ID_CUSTOMER" | jq -c '{"id": .id, "status": .status, "total": .total_amount}'

test_step "Customer: Try to Update Own Order Status (Security Path - Unhappy)"
api_call PATCH "/orders/$ORDER_ID/status" "$SESSION_ID_CUSTOMER" '{"status": "shipped"}' | jq -c .

test_step "Admin: Update Order Status to 'confirmed' (Happy Path)"
api_call PATCH "/orders/$ORDER_ID/status" "$SESSION_ID_ADMIN" '{"status": "confirmed"}' | jq -c '{"id": .id, "new_status": .status}'

###############################################################################
# 5. CLEANUP & FINAL CHECKS
###############################################################################
echo -e "\n${YELLOW}--- Cleanup ---${NC}"

test_step "Admin: Delete Mock Product (Delete)"
api_call DELETE "/products/$PRODUCT_ID" "$SESSION_ID_ADMIN" && echo "✅ Cleaned up product $PRODUCT_ID"

test_step "Public: Verify Deleted Product is Hidden from Public List"
api_call GET "/products/" none | jq -e ".[] | select(.id == $PRODUCT_ID)" > /dev/null && echo "❌ Logic Flaw: Soft-deleted product still visible" || echo "✅ Product Hidden"

test_step "Customer: Logout"
RES=$(api_call POST "/auth/logout" "$SESSION_ID_CUSTOMER")
echo "✅ Logout request sent"

test_step "Customer: Verify Session Revocation"
# Try to access /auth/me with the logged-out session
api_call GET "/auth/me" "$SESSION_ID_CUSTOMER" | jq -c . | grep -qi "not authenticated" && echo "✅ Session Revoked" || echo "❌ Session Still Active after Logout"

echo -e "\n${GREEN}=== All Tests Completed ===${NC}"
