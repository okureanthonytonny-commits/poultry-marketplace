# Products Module

Handles product management for the Limelight store.

## Overview

This module provides CRUD operations for products with soft delete, duplicate name prevention, and role‑based access control. Public endpoints are read‑only; admin endpoints require the user to have the `admin` role.

## Data Model

### `Product` (SQLModel table)

| Field        | Type      | Description                     |
|--------------|-----------|---------------------------------|
| `id`         | `int`     | Primary key                     |
| `name`       | `str`     | Product name, max length 255, indexed |
| `description`| `str?`    | Optional, max length 500        |
| `price`      | `float`   | Must be > 0                     |
| `stock`      | `int`     | Default 0, >= 0                 |
| `image_url`  | `str?`    | Optional image URL, max 500     |
| `deleted_at` | `datetime?`| Soft delete timestamp           |
| `created_at` | `datetime`| Creation time                   |
| `updated_at` | `datetime`| Auto‑updated on change          |

## Schemas (Pydantic)

- `ProductCreate`: used for creation (no `id`, `deleted_at`, `created_at`, `updated_at`)
- `ProductUpdate`: partial update (all fields optional)
- `ProductRead`: full read, includes `deleted_at` (used by admin)
- `ProductReadPublic`: excludes `deleted_at` (used by public endpoints)

## Services

Located in `services.py`:

- `create_product`: creates a product, checks for duplicate active name (409 Conflict)
- `get_product`: retrieve one product, optional `include_deleted`
- `list_products`: paginated list, optional `include_deleted`
- `update_product`: partial update, checks name uniqueness if name is changed
- `delete_product`: soft delete (default) or hard delete if `hard=True`
- `restore_product`: restores a soft‑deleted product

## API Endpoints

All endpoints are prefixed with `/api` in the main app.

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/products/` | Public list (only active products) | none |
| GET | `/products/{id}` | Public detail (only active) | none |
| POST | `/products/` | Create product | admin |
| GET | `/products/admin/all` | List all products (including deleted) | admin |
| GET | `/products/admin/{id}` | Get product (optionally deleted) | admin |
| PUT | `/products/admin/{id}` | Update product | admin |
| DELETE | `/products/admin/{id}` | Soft delete (or hard with ?hard=true) | admin |
| POST | `/products/admin/{id}/restore` | Restore deleted product | admin |

## Testing

Run the module tests:

```bash
cd backend
python -m pytest app/modules/products/tests/test_products.py -v# Products Module

Handles product management for the Limelight store.

## Overview

This module provides CRUD operations for products with soft delete, duplicate name prevention, and role‑based access control. Public endpoints are read‑only; admin endpoints require the user to have the `admin` role.

## Data Model

### `Product` (SQLModel table)

| Field        | Type      | Description                     |
|--------------|-----------|---------------------------------|
| `id`         | `int`     | Primary key                     |
| `name`       | `str`     | Product name, max length 255, indexed |
| `description`| `str?`    | Optional, max length 500        |
| `price`      | `float`   | Must be > 0                     |
| `stock`      | `int`     | Default 0, >= 0                 |
| `image_url`  | `str?`    | Optional image URL, max 500     |
| `deleted_at` | `datetime?`| Soft delete timestamp           |
| `created_at` | `datetime`| Creation time                   |
| `updated_at` | `datetime`| Auto‑updated on change          |

## Schemas (Pydantic)

- `ProductCreate`: used for creation (no `id`, `deleted_at`, `created_at`, `updated_at`)
- `ProductUpdate`: partial update (all fields optional)
- `ProductRead`: full read, includes `deleted_at` (used by admin)
- `ProductReadPublic`: excludes `deleted_at` (used by public endpoints)

## Services

Located in `services.py`:

- `create_product`: creates a product, checks for duplicate active name (409 Conflict)
- `get_product`: retrieve one product, optional `include_deleted`
- `list_products`: paginated list, optional `include_deleted`
- `update_product`: partial update, checks name uniqueness if name is changed
- `delete_product`: soft delete (default) or hard delete if `hard=True`
- `restore_product`: restores a soft‑deleted product

## API Endpoints

All endpoints are prefixed with `/api` in the main app.

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/products/` | Public list (only active products) | none |
| GET | `/products/{id}` | Public detail (only active) | none |
| POST | `/products/` | Create product | admin |
| GET | `/products/admin/all` | List all products (including deleted) | admin |
| GET | `/products/admin/{id}` | Get product (optionally deleted) | admin |
| PUT | `/products/admin/{id}` | Update product | admin |
| DELETE | `/products/admin/{id}` | Soft delete (or hard with ?hard=true) | admin |
| POST | `/products/admin/{id}/restore` | Restore deleted product | admin |

## Testing

Run the module tests:

```bash
cd backend
python -m pytest app/modules/products/tests/test_products.py -v

Tests cover:
    `Creation`, `duplicate name`, `retrieval`, `listing`
    `Update`, `soft delete`, `restore`
    All admin endpoints (using a test database)

## Notes
    Soft‑deleted products are hidden from public endpoints.
    Duplicate name check is case‑sensitive and applies only to active (not soft‑deleted) products.
    Admin role is required for all write endpoints; role check uses require_admin from core dependencies.