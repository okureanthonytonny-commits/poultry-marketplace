# Products Module – Tasks

## Completed

- [x] Define `Product` model (SQLModel)
- [x] Add `created_at` and `updated_at` timestamps with auto‑update
- [x] Add `deleted_at` for soft delete
- [x] Create Pydantic schemas: `ProductCreate`, `ProductRead`, `ProductUpdate`
- [x] Write services: create, get, list (with pagination), update, delete (soft/hard), restore
- [x] Implement router:
  - `GET /products/` – public list
  - `GET /products/{id}` – public detail
  - `POST /products/` – admin only
  - `PUT /products/admin/{id}` – admin only
  - `DELETE /products/admin/{id}` – admin only (soft delete)
  - `POST /products/admin/{id}/restore` – admin only
  - `GET /products/admin/all` – admin list (include deleted)
- [x] Write tests (services, endpoints) – 7 tests passing
- [x] Generate Alembic migration for `products` table

## Remaining / Future

- [ ] Add image upload (multipart form, cloud storage)
- [ ] Add search/filtering (by name, price range)
- [ ] Add product categories (many-to-many)
- [ ] Add product reviews/ratings
