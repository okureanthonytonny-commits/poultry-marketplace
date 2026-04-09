# Cart Module – Tasks

## Completed

- [x] Define `CartItem` model (SQLModel)
- [x] Add foreign keys to `users` and `products`
- [x] Create Pydantic schemas: `CartItemCreate`, `CartItemUpdate`, `CartItemRead`
- [x] Write services: `get_cart_items`, `add_to_cart`, `update_cart_item`, `remove_cart_item`, `clear_cart`
- [x] Implement router endpoints:
  - `GET /cart/` – get user's cart (enriched)
  - `POST /cart/items` – add item
  - `PUT /cart/items/{product_id}` – update quantity
  - `DELETE /cart/items/{product_id}` – remove item
  - `DELETE /cart/` – clear cart
- [x] Enrich cart items with product details
- [x] Stock validation during add/update
- [x] Write tests (services, endpoints) – included in integration tests
- [x] Alembic migration for `cart_items` table

## Remaining / Future

- [ ] Handle product deletion: automatically remove from cart
- [ ] Add cart expiry (e.g., remove after 30 days)
- [ ] Support for multiple carts (e.g., saved for later)
