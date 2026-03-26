# Products Module – Tasks

- [ ] Define `Product` model (SQLModel)
- [ ] Add `created_at` and `updated_at` timestamps with auto‑update
- [ ] Create Pydantic schemas: `ProductCreate`, `ProductRead`, `ProductUpdate`
- [ ] Write services: create, get, list (with pagination), update, delete
- [ ] Implement router:
  - `GET /api/products` – public list (pagination)
  - `GET /api/products/{id}` – public detail
  - `POST /api/admin/products` – admin only (image upload optional)
  - `PUT /api/admin/products/{id}` – admin only
  - `DELETE /api/admin/products/{id}` – admin only
- [ ] Add image upload endpoint (if not handled by admin frontend)
- [ ] Write tests (services, endpoints)
- [ ] Generate Alembic migration for `product` table
- [ ] Update root issues.md