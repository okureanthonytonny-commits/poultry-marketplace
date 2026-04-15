#!/bin/bash

# TEST API ENDPOINTS FOR LIMELIGHT V2
# Make sure: 1) Database is running: docker-compose up -d db
#            2) Uvicorn server is running: uvicorn app.main:app --reload

BASE_URL="https://limelight-v2.onrender.com"
HEADER_JSON="Content-Type: application/json"

echo "=== LIMELIGHT V2 API TEST SUITE ==="
echo "Base URL: $BASE_URL"
echo ""

# ============================================
# 1. HEALTH CHECK
# ============================================
echo "📋 1. HEALTH CHECK"
echo "GET /"
curl -s "$BASE_URL/" | jq .
echo ""
echo ""

# ============================================
# 2. PRODUCTS ENDPOINTS
# ============================================
echo "📦 2. PRODUCTS ENDPOINTS"
echo ""

echo "2.1 Get all products (public list, no auth required)"
echo "GET /products/"
curl -s "$BASE_URL/products/" | jq .
echo ""
echo ""

echo "2.2 Get specific product by ID (try ID 1)"
echo "GET /products/1"
curl -s "$BASE_URL/products/1" | jq .
echo ""
echo ""

echo "2.3 Create a product (ADMIN - will fail without auth, but shows endpoint)"
echo "POST /products/"
curl -s -X POST "$BASE_URL/products/" \
  -H "$HEADER_JSON" \
  -d '{
    "name": "Test Product",
    "description": "A test product",
    "price": 29.99,
    "stock": 10,
    "image_url": "https://example.com/image.jpg"
  }' | jq .
echo ""
echo ""

# ============================================
# 3. AUTH ENDPOINTS
# ============================================
echo "🔐 3. AUTH ENDPOINTS"
echo ""

echo "3.1 Get me (without cookie - should fail)"
echo "GET /auth/me"
curl -s "$BASE_URL/auth/me" | jq .
echo ""
echo ""

echo "3.2 Logout (without session - should fail gracefully)"
echo "POST /auth/logout"
curl -s -X POST "$BASE_URL/auth/logout" | jq .
echo ""
echo ""

echo "3.3 OAuth Google Login (get redirect)"
echo "GET /auth/login"
curl -s -L "$BASE_URL/auth/login" -I | head -20
echo ""
echo ""

# ============================================
# 4. CART ENDPOINTS
# ============================================
echo "🛒 4. CART ENDPOINTS"
echo ""

echo "4.1 Get cart (without auth - should fail)"
echo "GET /cart/"
curl -s "$BASE_URL/cart/" | jq .
echo ""
echo ""

echo "4.2 Add to cart (without auth - should fail)"
echo "POST /cart/items"
curl -s -X POST "$BASE_URL/cart/items" \
  -H "$HEADER_JSON" \
  -d '{
    "product_id": 1,
    "quantity": 1
  }' | jq .
echo ""
echo ""

# ============================================
# 5. ITEMS ENDPOINT
# ============================================
echo "📄 5. ITEMS ENDPOINT"
echo ""

echo "5.1 Get items"
echo "GET /items/"
curl -s "$BASE_URL/items/" | jq .
echo ""
echo ""

echo "5.2 Create item"
echo "POST /items/"
curl -s -X POST "$BASE_URL/items/" \
  -H "$HEADER_JSON" \
  -d '{
    "title": "Test Item",
    "description": "A test item"
  }' | jq .
echo ""
echo ""

# ============================================
# SUMMARY
# ============================================
echo "=== TEST SUMMARY ==="
echo "✅ Health check tested"
echo "✅ Products endpoints tested (public access)"
echo "✅ Auth endpoints tested (login requires OAuth flow)"
echo "✅ Cart endpoints tested (requires authentication)"
echo "✅ Items endpoints tested"
echo ""
echo "📝 NOTES:"
echo "  - Some endpoints require authentication (set via session cookie)"
echo "  - OAuth login requires Google OAuth credentials in .env"
echo "  - To test authenticated endpoints, you need a valid session_id cookie"
echo "  - Admin endpoints require 'admin' role"
echo ""
<Content of test_api.sh moved here, updated with BASE_URL check if needed>
