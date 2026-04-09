# Orders Module – Tasks

## Completed

- [x] Define `Order` and `OrderItem` models (SQLModel)
- [x] Add foreign keys to `users` and `products`
- [x] Use string for order status (pending, confirmed, shipped, delivered, cancelled)
- [x] Create Pydantic schemas: `OrderRead`, `OrderStatusUpdate`
- [x] Write services: `create_order_from_cart`, `get_user_orders`, `get_order`, `update_order_status`
- [x] Implement router endpoints:
  - `POST /orders/` – create order from cart (transaction, stock decrement, cart clear)
  - `GET /orders/` – list user's orders
  - `GET /orders/{order_id}` – get order details
  - `PATCH /orders/{order_id}/status` – admin only (update status)
- [x] Enrich orders with items and product details
- [x] Write tests (integration)
- [x] Alembic migrations for `orders` and `order_items` tables

## Remaining / Future

- [ ] Add order cancellation (with stock restoration)
- [ ] Add payment integration
- [ ] Add email notifications on status change
- [ ] Add order invoice PDF generation
