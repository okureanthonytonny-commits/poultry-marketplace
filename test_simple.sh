#!/bin/bash

BASE_URL="http://localhost:8000"

echo "========================================="
echo "LIMELIGHT V2 API ENDPOINT TESTS"
echo "========================================="
echo ""

# Test 1: Health check
echo "1️⃣  ROOT ENDPOINT (Health Check)"
echo "curl  GET $BASE_URL/"
curl -s "$BASE_URL/" && echo "" || echo "FAILED"
echo ""

# Test 2: Products list
echo "2️⃣  LIST PRODUCTS"  
echo "curl GET $BASE_URL/products/"
echo "---"
curl -s "$BASE_URL/products/" && echo "" || echo "FAILED"
echo ""

# Test 3: Get specific product (try ID 1)
echo "3️⃣  GET SINGLE PRODUCT (ID 1)"
echo "curl GET $BASE_URL/products/1"
echo "---"
curl -s "$BASE_URL/products/1" && echo "" || echo "FAILED"
echo ""

# Test 4: Auth - Get me (should fail)
echo "4️⃣  GET ME (No Auth - should fail)"
echo "curl GET $BASE_URL/auth/me"
echo "---"
curl -s "$BASE_URL/auth/me" && echo "" || echo "FAILED"
echo ""

# Test 5: Cart - Get cart (should fail)
echo "5️⃣  GET CART (No Auth - should fail)"
echo "curl GET $BASE_URL/cart/"
echo "---"
curl -s "$BASE_URL/cart/" && echo "" || echo "FAILED"
echo ""

# Test 6: Items list
echo "6️⃣  LIST ITEMS"
echo "curl GET $BASE_URL/items/"
echo "---"
curl -s "$BASE_URL/items/" && echo "" || echo "FAILED"
echo ""

echo "========================================="
echo "✅ TESTS COMPLETE"
echo "========================================="
