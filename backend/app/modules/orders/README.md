# Orders Module

Handles order creation from the user's cart, order history, and status management.

## Models

- `Order`: stores order header (user, status, timestamps)
- `OrderItem`: stores line items (product, quantity, price snapshot)

## Schemas (Pydantic)

- `OrderRead`: includes order items with product details (enriched)
- `OrderStatusUpdate`: used for admin status updates

## Services

- `create_order_from_cart`: validates stock, creates order, decrements stock, clears cart (transaction)
- `get_user_orders`: returns list of orders for a user (enriched in router)
- `get_order`: returns single order (with ownership check)
- `update_order_status`: updates order status with transition validation

## API Endpoints

All endpoints are mounted under `/api/orders` (prefix in `main.py`).

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST   | `/`      | Create order from cart | user |
| GET    | `/`      | List user orders | user |
| GET    | `/{order_id}` | Get order details | user (own) or admin |
| PATCH  | `/{order_id}/status` | Update order status | admin |

## Status Transitions

- `pending` → `confirmed` or `cancelled`
- `confirmed` → `shipped` or `cancelled`
- `shipped` → `delivered` or `cancelled`
- `delivered` → (none)
- `cancelled` → (none)

## Testing

Run integration tests with:

```bash
cd backend
python -m pytest app/modules/orders/tests/test_orders.py -v
