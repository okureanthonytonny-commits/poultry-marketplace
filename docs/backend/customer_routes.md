
# Limelight v2 – Customer API Reference

Base URL: `https://limelight-v2.onrender.com` (or `http://localhost:8000` for development)

All authenticated endpoints require the `session_id` cookie (sent automatically with `credentials: 'include'`).

## Authentication

| Method | Endpoint | Request Data | Response | Notes |
| -------- | ---------- | -------------- | ---------- | ------- |
| GET | `/auth/login` | none | Redirects to Google OAuth | No direct response; browser redirects to Google, then back to `/` with cookie set. |
| POST | `/auth/logout` | none (cookie) | `{"message": "Logged out"}` | Clears session cookie and soft‑deletes session. |
| GET | `/auth/me` | none (cookie) | `UserRead` object or `401` | Returns current user info. |

### UserRead Schema

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "role": "customer",
  "created_at": "2026-01-01T00:00:00",
  "updated_at": "2026-01-01T00:00:00"
}
```

## Products (Public)

| Method | Endpoint | Request Data | Response | Notes |
| -------- | ---------- | -------------- | ---------- | ------- |
| GET | `/products/` | `?skip=0&limit=100` (optional) | Array of `ProductReadPublic` | Paginated list of active products (not soft‑deleted). |
| GET | `/products/{id}` | none | `ProductReadPublic` or `404` | Single product detail. |

### ProductReadPublic Schema

```json
{
  "id": 1,
  "name": "Organic Eggs",
  "description": "Fresh farm eggs",
  "price": 5.99,
  "stock": 100,
  "image_url": "https://...",
  "created_at": "2026-01-01T00:00:00",
  "updated_at": "2026-01-01T00:00:00"
}
```

## Cart (Authenticated)

| Method | Endpoint | Request Data | Response | Notes |
| -------- | ---------- | -------------- | ---------- | ------- |
| GET | `/cart/` | none (cookie) | Array of `CartItemRead` | Returns enriched cart items (product details included). |
| POST | `/cart/items` | `{"product_id": 1, "quantity": 2}` | `CartItemRead` | Adds item; if already in cart, updates quantity. |
| PUT | `/cart/items/{product_id}` | `{"quantity": 5}` | `CartItemRead` | Updates quantity of existing item. |
| DELETE | `/cart/items/{product_id}` | none | `204 No Content` | Removes item from cart. |
| DELETE | `/cart/` | none | `204 No Content` | Clears entire cart. |

### CartItemRead Schema

```json
{
  "id": 10,
  "product_id": 1,
  "quantity": 2,
  "product_name": "Organic Eggs",
  "product_price": 5.99,
  "product_image_url": "https://...",
  "created_at": "...",
  "updated_at": "..."
}
```

## Orders (Authenticated)

| Method | Endpoint | Request Data | Response | Notes |
| -------- | ---------- | -------------- | ---------- | ------- |
| POST | `/orders/` | none (cookie) | `OrderRead` | Creates order from current cart, clears cart, decrements stock. |
| GET | `/orders/` | none (cookie) | Array of `OrderRead` | Lists user's orders (most recent first). |
| GET | `/orders/{id}` | none (cookie) | `OrderRead` or `404` | Single order detail. |

### OrderRead Schema

```json
{
  "id": 100,
  "user_id": 1,
  "status": "pending",
  "created_at": "...",
  "updated_at": "...",
  "items": [
    {
      "id": 1001,
      "product_id": 1,
      "quantity": 2,
      "price_snapshot": 5.99,
      "product_name": "Organic Eggs",
      "product_image_url": "https://..."
    }
  ]
}
```

## Error Responses

- `401 Unauthorized` – missing or invalid session cookie.
- `403 Forbidden` – insufficient permissions (admin only).
- `404 Not Found` – resource does not exist.
- `400 Bad Request` – invalid input (e.g., quantity exceeds stock).
- `409 Conflict` – duplicate product name, etc.

## Notes for Frontend

- Always include `credentials: 'include'` in `fetch` calls to send/receive cookies.
- For development, use `http://localhost:8000` as base URL (CORS already allows `http://localhost:5173`).
- The `session_id` cookie is `HttpOnly` – you cannot read it from JavaScript. Just rely on the browser to send it automatically.
- After login, the user is redirected to `/` (the frontend root). Your frontend should then call `/auth/me` to get user info.
